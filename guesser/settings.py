from pydantic import ValidationError
import typing
import os
from json.decoder import JSONDecodeError

from guesser.consts import JSON_SETTINGS_PATH
from guesser.models import Settings


def show_configuration():
    if os.path.isfile(JSON_SETTINGS_PATH):
        settings = get_settings_from_settings_file()
        print('\033[1m')
        if settings is not None:
            for item in settings:
                print(f'{item[0].upper()}: ', end='')
                if isinstance(item[1], list):
                    print('\n  ', end='')
                    print(*item[1], sep=',\n  ')
                else:
                    print(item[1])
        print('\033[0m')
        input('\nPress ENTER to go back.')
        
    else:
        print('The game have not being configured yet!')


def get_settings_from_settings_file():
    if os.path.isfile(JSON_SETTINGS_PATH):
        print('\nWait a few seconds...\nValidating settings...\n')
        try:
            settings = Settings.parse_file(JSON_SETTINGS_PATH)
            return settings
        
        except ValidationError:
            print('Sorry, your settings are incorrect, reconfigure the game.')
        except JSONDecodeError:
            print('The game have not being configured yet!')
    else:
        print('\nThe game have not being configured yet!')
    return None


def configure_game():
    settings = get_users_settings_from_input()
    if settings is not None:
        save_settings(settings)


def get_users_settings_from_input():
    SETTINGS_PROMPTS = {
    "players_number": "Enter the number of CONTENDERS: ",
    "players_names": "Enter the NAME of player {player_number}: ",
    "players_folders": "Enter the path to the directory with {player_name}'s music: ",
    "sample_duration": "Enter the duration of a song sample (in seconds): ",
    "repeats_number": 'Enter a number of repeat listens on each round (0 for infinite).\n: ',
    "clues_number": 'Enter a number of additional clue samples during the game.\n: ',
    "rounds_number": 'Enter a number of rounds you want to play.\n: '
    }
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

        except KeyboardInterrupt:
            print('\nOK, all changes dismissed.\n')
            settings = None
            break
        print()

    return settings


def save_settings(settings):
    json_object = settings.json(indent=4)
    with open(JSON_SETTINGS_PATH, 'w', encoding='utf-8') as json_file:
        json_file.write(json_object)
    print('Your configuration SAVED!\n')
