import os
from typing import List, Dict
from pydub import AudioSegment
from pydantic import BaseModel, validator

from guesser.utils import (
    get_all_audiofiles, find_maximum_number_of_audiofiles
    )

class Settings(BaseModel):
    
    players_number: int = 0
    players_names: List[str] = []
    players_folders: List[str] = []
    sample_duration: float = 0
    repeats_number: int = 0
    clues_number: int = 0
    rounds_number: int = 0

    class Config:
        validate_assignment = True


    @validator('players_number', 'rounds_number')
    def check_number_must_be_positive(cls, number):
        assert number > 0, 'Sorry, enter a positive number.'
        return number

    @validator('repeats_number', 'clues_number')
    def check_number_must_be_positive_or_zero(cls, number):
        assert number >= 0, 'Sorry, enter a positive number or zero.'
        return number
    
    @validator('sample_duration')
    def check_number_is_adequate(cls, number):
        assert number >= 0.25 or number <= 5, 'Sorry, enter a number between 0.25 and 5.'
        return number

    @validator('players_names', 'players_folders', each_item=True)
    def check_text_not_empty(cls, text):
        assert text.strip() != '', 'Sorry, this can not be blank.'
        return text.strip()

    @validator('players_names', each_item=True)
    def check_text_is_not_to_long(cls, text):
        assert len(text.strip()) <= 20, 'Sorry, there can not be more than 20 characters.'
        return text.strip()

    @validator('players_folders', each_item=True)
    def check_if_path_exists(cls, path):
        assert os.path.exists(path), 'Sorry, there is no such folder.'
        return path

    @validator('players_folders', each_item=True)
    def check_if_there_are_audiofiles(cls, path):
        songs_number = len(get_all_audiofiles(path))
        print('songs_added: +', songs_number)
        assert songs_number != 0, 'Sorry, there are no supported audiofiles in this folder.'
        return path
    
    @validator('rounds_number')
    def check_if_rounds_number_smaller_than_max_of_songs(cls, r_number, values):
        songs_number = find_maximum_number_of_audiofiles(values['players_folders'])
        assert songs_number >= r_number, 'Sorry, you do not have enough songs in your library.'
        return r_number


class Song(BaseModel):

    song_object: AudioSegment

    title: str
    artist: str
    album: str
    year: str

    path: str
    filename: str
    length: int
    sample_time: int
    samples: List[AudioSegment]

    class Config:
        arbitrary_types_allowed = True


class User(BaseModel):

    id: int
    name: str
    path: str
    songs: List[Song]


class Game(BaseModel):

    current_user_id: int = 0
    current_round: int = 1

    users: List[User]
    rounds: int
    sample_duration: float
    score: List[float]
    repeats: int = 0
    clues: List[int]
    clue_selected: int = 1

    max_repeats: int
    infinite_repeats: bool = False
    results: Dict[int, List[float]] = dict()
