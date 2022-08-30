from pydantic import ValidationError
from time import sleep
import typing
import os

from guesser.consts import JSON_SETTINGS_PATH
from guesser.models import Settings, User, Song, Game
from guesser.utils import (
    choose_random_songs, process_song
)


def show_configuration():
    if os.path.isfile(JSON_SETTINGS_PATH):
        settings = get_settings_from_settings_file()
        if settings is not None:
            for item in settings:
                print(f'{item[0].upper()}: ', end='')
                if isinstance(item[1], list):
                    print('\n  ', end='')
                    print(*item[1], sep=',\n  ')
                else:
                    print(item[1])
        input('\nPress ENTER to go back.')
        
    else:
        print('The game have not being configured yet!')


def get_settings_from_settings_file():
    if os.path.isfile(JSON_SETTINGS_PATH):
        print('Wait a few seconds... Validating settings...\n')
        try:
            settings = Settings.parse_file(JSON_SETTINGS_PATH)
            return settings
        except ValidationError as exc:
            print('Sorry, your settings are incorrect, reconfigure the game.')


def save_settings(settings):
    json_object = settings.json(indent=4)
    with open(JSON_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
        json_file.write(json_object)
    print('Your configuration SAVED!\n')


def initialize_game():
    settings = get_settings_from_settings_file()
    players_number = settings.players_number
    rounds = settings.rounds_number
    list_of_users = []
    for i in range(players_number):
        path = settings.players_folders[i]
        random_songs_paths = choose_random_songs(path, rounds)
        list_of_songs = []
        for song_path in random_songs_paths:
            pr_song = Song.parse_obj(process_song(song_path))
            list_of_songs.append(pr_song)
        user = User(
            id=i, name=settings.players_names[i],
            path=settings.players_folders[i],
            songs=list_of_songs
            )
        list_of_users.append(user)
    list_of_score = [0,] * players_number
    list_of_clues = [settings.clues_number] * players_number
    infinite_repeats = True if settings.repeats_number == 0 else False
    game = Game(
        users=list_of_users, rounds=rounds, 
        sample_duration=settings.sample_duration,
        score=list_of_score, max_repeats=settings.repeats_number + 1,
        infinite_repeats=infinite_repeats, clues=list_of_clues
        )
    return game


def configure_game():
    settings = get_users_settings_from_input()
    if settings is not None:
        save_settings(settings)

SETTINGS_PROMPTS = {
    "players_number": "Enter the number of CONTENDERS: ",
    "players_names": "Enter the NAME of player {player_number}: ",
    "players_folders": "Enter the path to the directory with {player_name}'s music: ",
    "sample_duration": "Enter the duration of a song sample (in seconds): ",
    "repeats_number": 'Enter a number of repeat listens on each round (0 for infinite).\n: ',
    "clues_number": 'Enter a number of additional clue samples during the game.\n: ',
    "rounds_number": 'Enter a number of rounds you want to play.\n: '
}


def get_users_settings_from_input():
    print()

    settings = Settings.construct()
    for field_name, field in Settings.__fields__.items():
        try:
            while True:
                type_ = field.outer_type_
                field_is_list = typing.get_origin(type_) is list

                values = []
                # if settings.n_players hasn't been initialised, it is a zero, and we still need at least one value
                n_values = max(settings.players_number, 1) if field_is_list else 1
                
                for value_idx in range(n_values):
                    player_number = value_idx + 1
                    player_name = settings.players_names[value_idx] if settings.players_names else ""

                    # input the value using the respective formatted prompt (or n_players values, if field is List[T])
                    prompt = SETTINGS_PROMPTS[field_name].format(player_number=player_number, player_name=player_name)
                    values.append(input(prompt))
                value = values if field_is_list else values[0]

                # actually validate and set the attribute in settings
                try:
                    setattr(settings, field_name, value)
                    break
                except ValidationError as exc:
                    for error in exc.raw_errors:
                        if isinstance(error, list):
                            print(f"{error[0][0].exc}\n({field_name}={value})", '\n')
                        else:
                            print(f"{error.exc}\n({field_name}={value})", '\n')
                    continue
        except KeyboardInterrupt as e:
            print('\nOK, all changes dismissed.\n')
            settings = None
            break
        print()

    return settings
