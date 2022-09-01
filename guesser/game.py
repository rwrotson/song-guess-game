from guesser.models import Song, User, Game
from guesser.settings import get_settings_from_settings_file
from guesser.metadata import handle_song
from guesser.utils import choose_random_songs, get_indexes_of_maximums_in_list


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
            pr_song = Song.parse_obj(handle_song(song_path, settings.sample_duration))
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


def show_current_state_of_game(game):
    current_user_id = game.current_user_id
    print(f'\n\033[1mROUND {game.current_round}\033[0m')
    for user in game.users:
        print(f'\033[1m{user.name}: {game.score[user.id]}\033[0m')
    username = game.users[current_user_id].name.upper()
    repeats = game.repeats
    clues = game.clues[current_user_id]
    print(f"\n\033[1m{username}'s turn.\033[0m")
    print(f'\033[1mrepeats: {repeats}, clues: {clues}\033[0m\n')


def show_game_results(game):

    input('\n\033[1mTHE GAME IS OVER!\n')

    winner_ids = get_indexes_of_maximums_in_list(game.score)
    for winner_id in winner_ids:
        winner = game.users[winner_id].name
        input(f'THE WINNER IS... {winner.upper()}')
    for user_id in range(0, len(game.users)):
        user = game.users[user_id]
        print(f"\n{user.name.upper()}'S RESULTS:")
        print(' ' * 20 + f'{game.score[user_id]} / {float(game.rounds)}')
        song_counter = 0
        for song in user.songs:
            print(game.results[user_id][song_counter], end=': ')
            print(f'{song.artist} -- {song.title}')
            song_counter += 1
    print('\033[0m')

    print('Press ENTER to return to main menu.')
