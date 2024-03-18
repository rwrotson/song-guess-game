import pickle
from dataclasses import dataclass, field
from enum import StrEnum, auto
from multiprocessing import Process
from pathlib import Path
from typing import Generator, Self

import music_tag
from pydub import effects

from app.cli.formatters import bold, TemplateString
from app.files import (
    AllowedFormats,
    get_audiofiles_paths,
    PlayableSegment,
    player_worker,
)
from app.game.representations import Score, ScoreItem
from app.game.selection import SONGS_STRATEGIES_MAPPING, SAMPLES_STRATEGIES_MAPPING
from app.settings.models import get_settings
from app.utils import Counter, get_singleton_instance


@dataclass(frozen=True, slots=True)
class Metadata:
    title: str
    artist: str
    album: str
    year: int
    track_number: int
    length: int

    @classmethod
    def from_path(cls, path: Path) -> Self:
        data = music_tag.load_file(path)

        metadata = {}
        for fld in cls.__annotations__.keys():
            try:
                altered_fld = fld.replace("_", "")
                metadata[fld] = data[altered_fld].values[0]
            except (KeyError, IndexError):
                metadata[fld] = None

        metadata["length"] = (int(data["#length"].values[0]) - 5) * 1000

        return cls(**metadata)

    def __str__(self):
        return f"{self.artist} — {bold(str(self.year))} — {self.album} — {bold(self.title)}"


class Sample:
    start_time: int
    sample: PlayableSegment
    times_played: int

    __slots__ = ("start_time", "sample", "times_played")

    def __init__(self, start_time: int, full_audio: PlayableSegment):
        normalized_audio = effects.normalize(full_audio)
        length = get_settings().game.sample_duration
        self.sample = normalized_audio[start_time : start_time + length * 1000]

        self.start_time = start_time
        self.times_played = 0

    def play(self):
        self.sample.play()
        self.times_played += 1


class Evaluation(StrEnum):
    DEFAULT = auto()
    FULL_ANSWER = auto()
    HALF_ANSWER = auto()
    WRONG_ANSWER = auto()
    NO_ANSWER = auto()

    def score(self, clues_used: int = 0) -> float:
        evaluation_settings = get_settings().evaluation
        score_mapping = {
            Evaluation.FULL_ANSWER: evaluation_settings.full_answer,
            Evaluation.HALF_ANSWER: evaluation_settings.half_answer,
            Evaluation.WRONG_ANSWER: evaluation_settings.wrong_answer,
            Evaluation.NO_ANSWER: evaluation_settings.no_answer,
        }
        discount = min(evaluation_settings.clue_discount * clues_used, 1)

        if (score := score_mapping[self]) > 0:
            return score * (1 - discount)

        return score


class Answer:
    _answer_prompt: str
    _clues_used: int
    _evaluation: Evaluation
    _score: float

    __slots__ = ("_answer_prompt", "_clues_used", "_evaluation", "_score")

    def __init__(self):
        self._answer_prompt: str = ""
        self._clues_used: int = 0
        self._evaluation: Evaluation = Evaluation.DEFAULT
        self._score: float = 0.0

    @property
    def answer_prompt(self) -> str:
        return self._answer_prompt

    @property
    def clues_used(self) -> int:
        return self._clues_used

    @property
    def evaluation(self) -> Evaluation:
        return self._evaluation

    @property
    def score(self) -> float:
        return self._score

    def use_clue(self) -> None:
        self._clues_used += 1

    def give_answer(self, answer_prompt: str) -> None:
        self._answer_prompt = answer_prompt

    def evaluate(self, evaluation: Evaluation) -> None:
        self._evaluation = evaluation
        self._score = evaluation.score(clues_used=self._clues_used)

    def __str__(self):
        return f"{self.answer_prompt} — {self.evaluation.name} — {self.score}"


@dataclass
class QuestionSong:
    audio: PlayableSegment
    metadata: Metadata
    question_sample: Sample
    clue_samples: list[Sample]
    answer: Answer

    last_clue_number: int = field(init=False)

    def __post_init__(self):
        self.last_clue_number = -1

    def play(self, start: int = 0) -> None:
        process = Process(target=player_worker, args=(self.audio, start))

        process.start()

        input("Press ENTER to stop.")
        print("\033[F\033[F\r")

        process.terminate()
        process.join()

    def play_sample(self) -> None:
        self.question_sample.play()

    def play_clue(self) -> None:
        from random import randint

        next_sample_strategy = get_settings().game.clues_strategy
        clue_number = -1
        if next_sample_strategy == "random_next":
            clue_number = randint(0, len(self.clue_samples) - 1)
        elif next_sample_strategy == "new_next":
            clue_number = (self.last_clue_number + 1) % len(self.clue_samples)
        self.last_clue_number = clue_number

        self.answer.use_clue()
        self.clue_samples[clue_number].play()

    @classmethod
    def from_path(cls, path: Path) -> Self:
        audio = PlayableSegment.from_path(path)
        metadata = Metadata.from_path(path)

        settings = get_settings()
        current_strategy = settings.sampling.strategy
        samples_strategy = SAMPLES_STRATEGIES_MAPPING[current_strategy](
            length=metadata.length,
            distance=int(settings.sampling.distance * 1000),
            quantity=settings.sampling.clues_quantity + 1,
            start=int(settings.sampling.from_ * 1000),
            end_cut=int(settings.sampling.to_finish * 1000),
        )
        start_times: list[int] = samples_strategy()

        return cls(
            audio=audio,
            metadata=metadata,
            question_sample=Sample(full_audio=audio, start_time=start_times[0]),
            clue_samples=[
                Sample(full_audio=audio, start_time=t) for t in start_times[1:]
            ],
            answer=Answer(),
        )

    def __str__(self):
        m = self.metadata
        return f"{m.artist} — {m.title} ({m.album}, {m.year})"


class Audiofile:
    path: Path
    filename: str
    format: AllowedFormats
    metadata: Metadata

    __slots__ = ("path", "filename", "format", "metadata")

    def __init__(self, path: Path):
        self.path = path
        self.filename = path.name
        self.format = AllowedFormats.from_path(path)
        self.metadata = Metadata.from_path(path)


class HelpUsage:
    repeats: Counter
    clues: Counter

    def __init__(self):
        settings = get_settings()
        max_repeats = settings.game.repeats_number
        max_clues = settings.game.clues_number

        self.repeats = Counter(min_v=0, max_v=max_repeats, start_v=max_repeats)
        self.clues = Counter(min_v=0, max_v=max_clues, start_v=max_clues)

    @classmethod
    def restore(cls, repeats: int, clues: int):
        instance = cls()
        instance.repeats.current = repeats
        instance.clues.current = clues
        return instance

    @property
    def repeats_left(self):
        return self.repeats.current

    @property
    def clues_left(self):
        return self.clues.current

    def __str__(self):
        repeats, clues = str(self.repeats_left), str(self.clues_left)
        return f"repeats: {bold(repeats)}, clues: {bold(clues)}\n"


class Player:
    id: int
    name: str
    library_path: Path
    audiofiles: set[Audiofile]
    songs: list[QuestionSong]

    help_usage: HelpUsage

    __slots__ = ("id", "name", "library_path", "audiofiles", "songs", "help_usage")

    def __init__(self, *, id_: int, name: str, library_path: Path | None) -> None:
        self.id: int = id_
        self.name: str = name
        self.library_path: Path = library_path

        self.audiofiles: set[Audiofile] = self.get_all_audiofiles()
        self.songs: list[QuestionSong] = []

        self.help_usage: HelpUsage = HelpUsage()

    def get_all_audiofiles(self) -> set[Audiofile]:
        if not self.library_path:
            return set()
        audiofiles_paths = get_audiofiles_paths(self.library_path)
        return {Audiofile(path=Path(path)) for path in audiofiles_paths}

    def initialize_songs(self):
        current_strategy = get_settings().selection.strategy
        strategy_function = SONGS_STRATEGIES_MAPPING[current_strategy]()

        quantity = get_settings().game.rounds_number
        chosen_audiofiles = strategy_function(
            audiofiles=list(self.audiofiles), quantity=quantity
        )

        self.songs = [QuestionSong.from_path(file.path) for file in chosen_audiofiles]

    def get_library_short_repr(self) -> str:
        header = f"{bold(self.name)} (id={self.id + 1}): {str(self.library_path)}"
        count = f"\t{bold(str(len(self.audiofiles)))} audiofiles found in library."
        return f"{header}\n{count}\n"

    def get_library_extended_repr(self) -> str:
        metadata_list = [Metadata.from_path(f.path) for f in self.audiofiles]
        metadata_list.sort(
            key=lambda x: (x.artist, x.year, x.album, x.track_number, x.title),
        )

        short_repr = self.get_library_short_repr()

        details = "\n"
        if len(self.audiofiles):
            details = "\n".join(
                [("\t\t" + str(metadata)) for metadata in metadata_list]
            )

        return f"{short_repr}{details}\n"


class GameCounter:
    _current_player_id: int  # counting from 0
    _current_round: int  # counting from 0

    __slots__ = (
        "_current_player_id",
        "_current_round",
        "_players_counter",
        "_rounds_counter",
        "_is_first_cycle",
    )

    def __init__(
        self, players: int, rounds: int, start_player: int = 0, start_round: int = 0
    ) -> None:
        self._is_first_cycle = True
        self._players_counter = self._players_counter_gen(
            players, start_value=start_player
        )
        self._rounds_counter = self._rounds_counter_gen(rounds, start_value=start_round)

        next(self)

    @property
    def current_player_id(self) -> int:
        return self._current_player_id

    @property
    def current_round(self) -> int:
        return self._current_round

    def _players_counter_gen(
        self, players_number: int, start_value: int = 0
    ) -> Generator[int, None, None]:
        if start_value and self._is_first_cycle:
            for i in range(start_value):
                yield i
            self._is_first_cycle = False

        while True:
            for i in range(players_number):
                yield i

    @staticmethod
    def _rounds_counter_gen(
        rounds_number: int, start_value: int = 0
    ) -> Generator[int, None, None]:
        for i in range(start_value, rounds_number):
            yield i

    def __next__(self):
        self._current_player_id = next(self._players_counter)
        if self._current_player_id == 0:
            self._current_round = next(self._rounds_counter)
        return self

    def __str__(self):
        return f"Round {self.current_round}, Player {self.current_player_id}"


class GameStatus(StrEnum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    PAUSED = auto()
    FINISHED = auto()


class Game:
    rounds: int
    players: list[Player]
    counter: GameCounter
    status: GameStatus

    __slots__ = ("rounds", "players", "counter", "status")

    def __init__(self, players: list[Player], rounds: int) -> None:
        self.status = GameStatus.NOT_STARTED
        self.reset_game(players, rounds)

    def reset_game(self, players: list[Player], rounds: int) -> None:
        self.players, self.rounds = players, rounds
        self.counter = GameCounter(players=len(players), rounds=rounds)
        self.status = GameStatus.NOT_STARTED

    def initialize_songs(self):
        for player in self.players:
            player.initialize_songs()

    @property
    def current_round(self) -> int:
        return self.counter.current_round

    @property
    def current_player(self) -> Player:
        return self.players[self.counter.current_player_id]

    @property
    def current_song(self) -> QuestionSong:
        return self.current_player.songs[self.current_round]

    def next_iteration(self):
        next(self.counter)

        self.current_player.help_usage.repeats.reset()

    def get_score(self) -> TemplateString:
        score = Score(
            items=[
                ScoreItem(
                    player_id=player.id,
                    player_name=player.name,
                    score=sum([q.answer.score for q in player.songs if q.answer]),
                )
                for player in self.players
            ],
            current_round=self.counter.current_round,
            current_player_id=self.counter.current_player_id,
        )
        return score.representation

    def get_current_player_stats(self) -> TemplateString:
        return TemplateString(
            "${clr_current}${b}${player_name}${r}'s turn!\n${help_usage}",
        ).safe_substitute(
            player_name=self.current_player.name.upper(),
            help_usage=self.current_player.help_usage,
        )

    def get_endgame_stats(self):
        score = self.get_score()

        game_summary = TemplateString("\n")
        for round_number in range(self.rounds):
            game_summary += TemplateString(
                "${b}ROUND ${round_n}${r}\n",
            ).safe_substitute(
                round_n=round_number + 1,
            )

            for i, player in enumerate(self.players):
                song = player.songs[round_number]

                game_summary += TemplateString(
                    "${clr_n}${b}${player_name}${r}: "
                    "${song} | "
                    "${b}${evaluation}${r} | "
                    "${clr_n}${b}${score}${r} | "
                    "${clues_used}\n",
                ).safe_substitute(
                    clr_n=f"$clr_{i + 1}",
                    player_name=player.name,
                    song=str(song),
                    evaluation=song.answer.evaluation.upper(),
                    score=song.answer.score,
                    clues_used=song.answer.clues_used,
                )

            game_summary += "=" * 20 + "\n\n"

        return score + "\n" + game_summary

    @classmethod
    def from_settings(cls):
        settings = get_settings().load_from_file()

        game = cls(
            players=[
                Player(id_=i, name=player.name, library_path=player.path)
                for i, player in enumerate(settings.players)
            ],
            rounds=settings.game.rounds_number,
        )
        cls._instance = game

        return game

    @classmethod
    def from_pickle(cls) -> Self | None:
        pickle_path = get_settings().service_paths.game_pickle_path
        try:
            with open(pickle_path, "rb") as file:
                game = pickle.load(file)
                cls._instance = game
                return game
        except FileNotFoundError:
            return None

    def pickle(self) -> None:
        pickle_path = get_settings().service_paths.game_pickle_path
        with open(pickle_path, "wb") as file:
            pickle.dump(self, file)


def get_game() -> Game:
    return get_singleton_instance(Game)


class History:
    def __init__(self, *, game: Game):
        self.answers = {}

    def score_for_player_id(self, player_id: int, /) -> list[float]:
        pass

    def score_for_round(self, round_number: int, /) -> list[float]:
        pass
