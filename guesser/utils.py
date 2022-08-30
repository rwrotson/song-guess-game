from time import sleep
import random
import os
from pathlib import Path
import vlc
import magic
import music_tag


def get_all_audiofiles(path):
    if path is None:
        return None
    ALLOWED_FORMATS = ['audio/x-flac', 'audio/mpeg', 'audio/x-wav']
    all_files = []
    for path, _, files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(path, file))
    audio_files = [f for f in all_files if magic.from_file(f, mime=True) in ALLOWED_FORMATS]
    return audio_files


def find_maximum_number_of_audiofiles(paths):
    max = 0
    for path in paths:
        songs_number = len(get_all_audiofiles(path))
        if songs_number is None: 
            return None
        if songs_number > max: max = songs_number
    return max


def get_random_times_for_sampling(length):
    timestamps = []
    for _ in range(0, 2):
        while True:
            sample_start_time = random.randrange(1, length)
            for timestamp in timestamps:
                t_difference = abs(timestamp - sample_start_time)
                if  t_difference < 7000:
                    break
            timestamps.append(sample_start_time)
            break
    return timestamps


def choose_random_songs(path, number):
    audio_files = get_all_audiofiles(path)
    chosen = random.sample(audio_files, number)
    return chosen


def process_song(path):
    metadata = get_metadata_from_song_path(path)
    length = int(metadata['length'])
    samples = get_random_times_for_sampling(length)
    metadata['samples'] = samples
    return metadata


def get_metadata_from_song_path(path):
    filename = Path(path).name
    metadata = {'path': path, 'filename': filename}

    data = music_tag.load_file(path)
    FIELDS = ('title', 'artist', 'album', 'year')
    for field in FIELDS:
        try:
            metadata[field] = data[field].values[0]
        except IndexError:
            metadata[field] = None

    metadata['length'] = (int(data['#length'].values[0]) - 5) * 1000

    return metadata


def play_song_sample(path, start, length, pre=0, ext=0):
    song = vlc.MediaPlayer(path)
    song.play()
    actual_start = start - pre if start - pre > 0 else 0
    song.set_time(actual_start)
    sleep(length + ext)
    song.stop()


def play_song(path):
    song = vlc.MediaPlayer(path)
    song.play()
    input('Press ENTER to turn off the song.')
    song.stop()
