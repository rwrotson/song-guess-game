import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol


def get_indexes_of_maximums_in_list(list_object: list[Any]) -> list[int]:
    maximum = 0
    max_index_list = [0,]
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

    def __call__(self, audiofiles: list[Path], quantity: int) -> list[Path]:
        ...


class NaiveSongSelectionStrategy(SongSelectionStrategy):
    """
    Algorithm:
    Simple random selection of "quantity" audiofiles from given list.
    """

    literal: str = "naive"

    def __call__(self, audiofiles: list[Path], quantity: int) -> list[Path]:
        return random.sample(audiofiles, quantity)


class NormalizedSongSelectionStrategy(SongSelectionStrategy):
    """
    Algorithm:
    Normalize the list of audiofiles by its folder structure
    """

    literal: str = "normalized"

    def __call__(self, audiofiles: Iterable[Path], quantity: int) -> list[Path]:
        files_by_folders: dict[Path, set[Path]] = dict()
        for file in audiofiles:
            if file.parent not in files_by_folders:
                files_by_folders[file.parent] = set()
            files_by_folders[file.parent].add(file)

        folders = list(files_by_folders.keys())
        random.shuffle(folders)

        folder_counter = 1
        selected_files = []
        while len(selected_files) < quantity:

            if folder_counter >= len(folders):
                folder_counter = 1

            selected_folder = folders[folder_counter]

            while not files_by_folders[selected_folder]:
                folder_counter += 1

            selected_file = random.sample(files_by_folders[selected_folder], 1)[0]
            selected_files.append(selected_file)

            folder_counter += 1

        return selected_files


@dataclass
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
    times: int
    from_: int = 0
    left_to_finish: int = 0

    literal: str | None = None

    def __post_init__(self):
        if self.left_to_finish > self.length:
            raise ValueError("Left to finish cannot be greater than length.")

        self.to = self.length - self.left_to_finish
        if (self.to - self.from_) < self.distance * self.times:
            raise ValueError(
                f"Cannot fit {self.times} samples "
                f"of length {self.distance} "
                f"between {self.from_} and {self.to}."
            )

    @abstractmethod
    def __call__(self) -> list[int]:
        ...


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
        for _ in range(self.times):
            while True:
                sample_start_time = random.randrange(self.from_, self.to)

                is_remote_enough = True
                for timestamp in timestamps:  # check distance to other timestamps
                    t_difference = abs(timestamp - sample_start_time)
                    if t_difference < self.distance:
                        is_remote_enough = False
                        break

                if is_remote_enough:
                    timestamps.append(sample_start_time)
                    break

        return timestamps


class NormalizedRandomTimesStrategy(RandomTimesStrategy):
    """
    Algorithm:
    1. Segment "from_ -- to" is divided into `times` equal parts.
    2. For each part, a random number is generated.
    """

    literal = "normalized"

    def __call__(self) -> list[int]:
        step = (self.to - self.from_) // self.times
        segment_start, segment_end = self.from_, self.from_ + step

        timestamps = []
        while segment_end < self.to - self.length:
            timestamp = random.randrange(segment_start, segment_end - self.length)
            timestamps.append(timestamp)
            segment_start, segment_end = segment_end, segment_end + step

        return timestamps
