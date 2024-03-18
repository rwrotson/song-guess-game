import random
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Protocol, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.models import Audiofile


def get_indexes_of_maximums_in_list(list_object: list[Any]) -> list[int]:
    maximum = 0
    max_index_list = [0]
    for element_number in range(0, len(list_object)):
        if list_object[element_number] > maximum:
            maximum = list_object[element_number]
            max_index_list = [element_number]
        elif list_object[element_number] == maximum:
            max_index_list.append(element_number)
    return max_index_list


class SongSelectionStrategy(Protocol):
    """
    Returns a list of random audiofile from given list of audiofiles.
    """

    def __call__(
        self,
        audiofiles: Sequence["Audiofile"],
        quantity: int,
    ) -> list["Audiofile"]: ...


class NaiveSongSelectionStrategy:
    """
    Algorithm:
    Simple random selection of "quantity" audiofiles from given list.
    """

    literal: str = "naive"

    def __call__(
        self, audiofiles: Sequence["Audiofile"], quantity: int
    ) -> list["Audiofile"]:
        return random.sample(audiofiles, quantity)


def _select_by(
    files_by_key: dict[str, set["Audiofile"]], quantity: int
) -> list["Audiofile"]:
    keys = list(files_by_key.keys())  # TODO: rename function
    random.shuffle(keys)

    key_counter = 1
    selected_files: list["Audiofile"] = []
    while len(selected_files) < quantity:
        if key_counter >= len(keys):
            key_counter = 1

        selected_key = keys[key_counter]

        while not files_by_key[selected_key]:
            key_counter += 1

        selected_file = random.sample(files_by_key[selected_key], 1)[0]
        selected_files.append(selected_file)

        selected_key += 1

    return selected_files


class NormalizedByFolderSongSelectionStrategy:
    """
    Algorithm:
    Normalize the list of audiofiles by folder structure,
    so selected audiofiles are homogeneously distributed across the folders.
    """

    literal: str = "normalized_by_folder"

    def __call__(
        self, audiofiles: Sequence["Audiofile"], quantity: int
    ) -> list["Audiofile"]:
        files_by_folders: dict[str, set["Audiofile"]] = dict()
        for audiofile in audiofiles:
            parent_path = str(audiofile.path.parent)
            if audiofile.path.parent not in files_by_folders:
                files_by_folders[parent_path] = set()
            files_by_folders[parent_path].add(audiofile)

        return _select_by(files_by_key=files_by_folders, quantity=quantity)


class NormalizedByAlbumSongSelectionStrategy:
    """
    Algorithm:
    Normalize the list of audiofiles by theirs metadata,
    so selected audiofiles are homogeneously distributed across the albums.
    """

    literal: str = "normalized_by_album"

    def __call__(
        self, audiofiles: Sequence["Audiofile"], quantity: int
    ) -> list["Audiofile"]:
        files_by_albums: dict[str, set["Audiofile"]] = dict()
        for audiofile in audiofiles:
            album = audiofile.metadata.album
            if album not in files_by_albums:
                files_by_albums[album] = set()
            files_by_albums[album].add(audiofile)

        return _select_by(files_by_key=files_by_albums, quantity=quantity)


class RandomTimesStrategy(ABC):
    """
    Returns a list of random timestamps for sampling.

    For given length of sample, calculates a list of timestamps
    on the segment between from_ and to,
    so the distance between samples is at least `distance`.

    Usage: ConcreteRandomTimesStrategy(length, distance, times, from_, to)()
    """

    length: int
    distance: int
    quantity: int
    start: int = 0
    end_cut: int = 0

    literal: str | None = None

    def __init__(
        self,
        *,
        length: int,
        distance: int,
        quantity: int,
        start: int = 0,
        end_cut: int = 0,
    ):
        self.length = length  # full length of the track
        self.distance = distance  # minimal distance between samples
        self.quantity = quantity  # number of samples to select
        self.start = start  # start of the segment
        self.end_cut = end_cut  # number of ms to cut from the end
        self.end = self.length - self.end_cut  # end point of the segment

        try:
            if end_cut + start > length:
                raise ValueError(
                    {
                        "flag": "LEN",
                        "msg": "Start and end_cut values too big for the track.",
                    }
                )
            if (length - start - end_cut) < distance * quantity:
                raise ValueError(
                    {
                        "flag": "DIS",
                        "msg": "Cannot fit samples of given length and distance.",
                    }
                )

        except ValueError as e:
            if (flag := e.args[0].get("flag")) == "DIS":
                self.__call__ = partial(
                    self.fallback_algorithm,
                    quantity=self.quantity,
                )
            elif flag == "LEN":
                self.__call__ = partial(
                    self.fallback_algorithm_for_full_length,
                    quantity=self.quantity,
                )
            else:
                raise e

    def fallback_algorithm(self, quantity: int) -> list[int]:
        return [random.randrange(self.start, self.end) for _ in range(quantity)]

    def fallback_algorithm_for_full_length(self, quantity: int) -> list[int]:
        return [random.randrange(self.length) for _ in range(quantity)]

    @abstractmethod
    def __call__(self) -> list[int]: ...


class NaiveRandomTimesStrategy(RandomTimesStrategy):
    """
    Algorithm:
    1. Select random number from "from_ -- to" segment.
    2. Check the distance between this number and all previous numbers is smaller than "distance"
    3. If it is, repeat step 1, else append the number to the list of timestamps.

    Use with cautios with short length and high distance or time, it can produce long loops.
    """

    literal = "naive"

    def __call__(self) -> list[int]:
        timestamps = []
        for _ in range(self.quantity):
            for i in range(25):
                sample_start_time = random.randrange(self.start, self.end)

                is_remote_enough = True
                for timestamp in timestamps:  # check distance to other timestamps
                    t_difference = abs(timestamp - sample_start_time)
                    if t_difference < self.distance:
                        is_remote_enough = False
                        break

                if is_remote_enough:
                    timestamps.append(sample_start_time)
                    break

        if (diff := self.quantity - len(timestamps)) > 0:
            timestamps.append(self.fallback_algorithm(diff))

        return timestamps


class NormalizedRandomTimesStrategy(RandomTimesStrategy):
    """
    Algorithm:
    1. Segment "from_ -- to" is divided into `times` equal parts.
    2. For each part, a random number is generated.
    """

    literal = "normalized"

    def __call__(self) -> list[int]:
        step = (self.end - self.start) // self.quantity
        segment_start, segment_end = self.start, self.start + step

        timestamps = []
        while segment_end < self.end:
            timestamp = random.randrange(segment_start, segment_end)
            timestamps.append(timestamp)
            segment_start, segment_end = segment_end, segment_end + step

        return timestamps


SONGS_STRATEGIES_MAPPING: dict[str, type[SongSelectionStrategy]] = {  # noqa
    "naive": NaiveSongSelectionStrategy,
    "normalized_by_folder": NormalizedByFolderSongSelectionStrategy,
    "normalized_by_album": NormalizedByAlbumSongSelectionStrategy,
}


SAMPLES_STRATEGIES_MAPPING: dict[str, type[RandomTimesStrategy]] = {
    "naive": NaiveRandomTimesStrategy,
    "normalized": NormalizedRandomTimesStrategy,
}
