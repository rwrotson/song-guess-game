import sys

from guesser.consts import READMES
from guesser.settings import show_configuration, configure_game
from guesser.game import (
    initialize_game, show_current_state_of_game, show_game_results
)
from guesser.player import play_sample, play_song


def create_menu(options, functions_dict, game=None):
    options_number = len(functions_dict)
    try:
        option = input(options).strip()

        try:
            option = int(option)
        except ValueError:
            print(f'Please ENTER a number between 1 and {options_number}.\n')
            game = create_menu(options, functions_dict, game=game)
            return game

        if 0 < option <= options_number:
            func = functions_dict[str(option)].get('func')
            params = functions_dict[str(option)].get('params')
            if isinstance(params, tuple):
                func(*params)
            elif params is not None:
                func(params)
            else:
                func()
        else:
            print(f'Please ENTER a number between 1 and {options_number}.\n')
            game = create_menu(options, functions_dict, game=game)
        return game

    except KeyboardInterrupt:
        print('\nOK, goodbye!\n')
        sys.exit()


def create_main_menu():
    MAIN_OPTIONS = '''\nEnter the number of ACTION you want me to do:
            1. SHOW current configuration.
            2. CONFIGURE the game.
            3. PLAY the game with previous configuration.
            4. Get HELP.
            5. EXIT.\n: '''

    MAIN_FUNCTIONS = {
        '1': {
            'func': show_configuration
        },
        '2': {
            'func': configure_game
        },
        '3': {
            'func': create_game_menu
        },
        '4': {
            'func': create_help_menu
        },
        '5': {
            'func': sys.exit,
        }
    }
    create_menu(MAIN_OPTIONS, MAIN_FUNCTIONS)


def create_game_menu():
    game = initialize_game()
    for game_round in range(1, game.rounds + 1):
        for user_id in range(0, len(game.users)):
            game.current_round = game_round
            game.current_user_id = user_id
            game.repeats = game.max_repeats
            game = create_round_menu(game)
    show_game_results(game)


def create_round_menu(game):
    show_current_state_of_game(game)
    
    GAME_OPTIONS = '''\nEnter the number of ACTION:
            1. PLAY or REPEAT sample.
            2. Get a CLUE.
            3. Give an ANSWER.\n: '''
    GAME_FUNCTIONS = {
        '1': {
            'func': play_or_repeat_sample,
            'params': game
        },
        '2': {
            'func': get_a_clue,
            'params': game
        },
        '3': {
            'func': create_answer_menu,
            'params': game
        }
    }
    game = create_menu(GAME_OPTIONS, GAME_FUNCTIONS, game)
    return game


def play_or_repeat_sample(game):
    song = game.users[game.current_user_id].songs[game.current_round - 1]
    if game.repeats > 0:
        play_sample(song.samples[0])
        if game.infinite_repeats is False and game.repeats != 0:
            game.repeats -= 1
    else:
        print('You are out of attempts to listen! Answer or pass!\n')
    game = create_round_menu(game)
    return game


def get_a_clue(game):
    if game.clue_selected == 10: game.clue_selected = 1
    song = game.users[game.current_user_id].songs[game.current_round - 1]
    if game.clues[game.current_user_id] > 0:
        play_sample(song.samples[game.clue_selected])
        game.clue_selected += 1
    else:
        print('You are out of clues! Answer or pass!\n')
    if game.clues[game.current_user_id] != 0:
        game.clues[game.current_user_id] -= 1
    game = create_round_menu(game)
    return game


def create_answer_menu(game):
    try:
        answer = input('''\nPrint your suggestion about this song,
        or say it aloud to your contenders and press ENTER.\n: ''')
    except KeyboardInterrupt:
        print('OK, going back...')
        game = create_round_menu(game)
        return game
    game = create_evaluation_menu(game, answer)
    return game


def create_evaluation_menu(game, answer=''):
    if answer.strip() == '': answer = 'no answer'
    song = game.users[game.current_user_id].songs[game.current_round - 1]
    song_repr = f'\033[1m{song.artist} - {song.title}\n({song.album}, {song.year})\033[0m'
    print(f'\nYour answer is:\n\033[1m{answer}\033[0m,\nwhile actually it is:\n{song_repr}\n')

    EVALUATION_OPTIONS = '''\nEnter the number of ACTION you want me to do:
    1. LISTEN to EXTENDED sample.
    2. LISTEN the song ENTIRELY.
    3. Give 1 POINT for the answer.
    4. Give 0.5 POINTS for the answer.
    5. Give 0 POINTS for the answer.\n: '''
    EVALUATION_FUNCTIONS = {
        '1': {
            'func': play_extended_sample,
            'params': (game, answer)
        },
        '2': {
            'func': play_full_song,
            'params': (game, answer)
        },
        '3': {
            'func': change_score,
            'params': (game, 1.0)
        },
        '4': {
            'func': change_score,
            'params': (game, 0.5)
        },
        '5': {
            'func': change_score,
            'params': (game, 0.0)
        }
    }
    game = create_menu(EVALUATION_OPTIONS, EVALUATION_FUNCTIONS)
    return game


def play_extended_sample(game, answer):
    song = game.users[game.current_user_id].songs[game.current_round - 1]
    play_song(song.song_object, song.sample_time)
    game = create_evaluation_menu(game, answer)
    return game


def play_full_song(game, answer):
    song = game.users[game.current_user_id].songs[game.current_round - 1]
    play_song(song.song_object)
    game = create_evaluation_menu(game, answer)
    return game


def change_score(game, points):
    game.score[game.current_user_id] += points
    if game.results.get(game.current_user_id) is None:
        game.results[game.current_user_id] = [points]
    else:
        game.results[game.current_user_id].append(points)
    return game


def create_help_menu():
    HELP_OPTIONS = '''\nEnter the number of ACTION you want me to do:
            1. Game RULES.
            2. Help with SETTINGS.
            3. BACK.\n: '''

    HELP_FUNCTIONS = {
        '1': {
            'func': input,
            'params': READMES['rules']
        },
        '2': {
            'func': input,
            'params': READMES['settings']
        },
        '3': {
            'func': print,
        }
    }
    create_menu(HELP_OPTIONS, HELP_FUNCTIONS)
