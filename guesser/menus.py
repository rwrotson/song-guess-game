from guesser.settings_menu import show_configuration, configure_game, initialize_game
from guesser.consts import READMES
from guesser.utils import play_song_sample, play_song


def create_menu(options, functions_dict, game=None):
    options_number = len(functions_dict)
    try:
        option = input(options).strip()

        try:
            option = int(option)
        except ValueError:
            print(f'Please ENTER a number between 1 and {options_number}.\n')
            game = create_menu(options, functions_dict, game=None)
            return game

        if option < options_number and option > 0:
            func = functions_dict[str(option)].get('func')
            params = functions_dict[str(option)].get('params')
            if isinstance(params, tuple):
                func(*params)
            elif params is not None:
                func(params)
            else:
                func()
        return game

    except KeyboardInterrupt as e:
        print('\nOK, goodbye!\n')
        exit()


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
            'func': create_main_menu
        }
    }
    create_menu(HELP_OPTIONS, HELP_FUNCTIONS)


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
            'func': exit,
        }
    }
    create_menu(MAIN_OPTIONS, MAIN_FUNCTIONS)


def create_game_menu():
    game = initialize_game()
    for round in range(1, game.rounds + 1):
        for user_id in range(0, len(game.users)):
            game.round = round
            game.current_user_id = user_id
            game.repeats = game.max_repeats
            game = create_round_menu(game)
    show_game_results(game)


def create_round_menu(game):
    show_current_state_of_game(game)
    
    GAME_OPTIONS = '''\nEnter the number of ACTION:
            1. PLAY or REPEAT sample.
            2. Get a CLUE.
            3. Give an ANSWER.
            4. PASS this round.\n: '''
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
        },
        '4': {
            'func': create_evaluation_menu,
            'params': game
        }
    }
    game = create_menu(GAME_OPTIONS, GAME_FUNCTIONS, game)
    return game


def show_current_state_of_game(game):
    current_user_id = game.current_user_id
    print(f'\n\033[1mROUND {game.round}\033[0m')
    for user in game.users:
        print(f'\033[1m{user.name}: {game.score[user.id]}\033[0m')
    username = game.users[current_user_id].name.upper()
    repeats = game.repeats
    clues = game.clues[current_user_id]
    print(f"\n\033[1m{username}'s turn.\033[0m")
    print(f'\033[1mrepeats: {repeats}, clues: {clues}\033[0m\n')


def play_or_repeat_sample(game):
    song = game.users[game.current_user_id].songs[game.round]
    if game.repeats > 0:
        play_song_sample(song.path, song.samples[0], game.sample_duration)
        if game.infinite_repeats is False and game.repeats != 0:
            game.repeats -= 1
    else:
        print('You are out of attempts to listen! Answer or pass!\n')
    game = create_round_menu(game)
    return game


def get_a_clue(game):
    song = game.users[game.current_user_id].songs[game.round]
    if game.clues[game.current_user_id] > 0:
        play_song_sample(song.path, song.samples[1], game.sample_duration)
    else:
        print('You are out of clues! Answer or pass!\n')
    game.clues[game.current_user_id] -= 1
    game = create_round_menu(game)
    return game


def create_answer_menu(game):
    answer = input('''\nPrint your suggestion about this song,
    or say it aloud to your contenders and press ENTER.\n:''')
    game = create_evaluation_menu(game, answer)


def create_evaluation_menu(game, answer=''):
    print(game, answer, sep='\n')
    if answer.strip() == '': answer = 'no answer'
    song = game.users[game.current_user_id].songs[game.round]
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
            'func': play_ext_sample,
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


def play_ext_sample(game, answer):
    song = game.users[game.current_user_id].songs[game.round]
    play_song_sample(song.path, song.samples[0], game.sample_duration, 5, 10)
    game = create_evaluation_menu(game, answer)
    return game


def play_full_song(game, answer):
    song = game.users[game.current_user_id].songs[game.round]
    play_song(song.path)
    game = create_evaluation_menu(game, answer)
    return game


def change_score(game, points):
    game.score[game.current_user_id] += points
    return game


def show_game_results(game):
    pass