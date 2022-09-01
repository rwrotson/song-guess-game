import random
import os

import magic


def get_indexes_of_maximums_in_list(list_object):
    maximum = 0
    max_index_list = [0,]
    for element_number in range(0, len(list_object)):
        if list_object[element_number] > maximum:
            maximum = list_object[element_number]
            max_index_list = [element_number]
        elif list_object[element_number] == maximum:
            max_index_list.append(element_number)
    return max_index_list


def get_all_audiofiles(path):
    ALLOWED_FORMATS = ['audio/x-flac', 'audio/mpeg', 'audio/x-wav']

    if path is None: return None
    all_files = []
    for path, _, files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(path, file))
    audio_files = [f for f in all_files if magic.from_file(f, mime=True) in ALLOWED_FORMATS]
    return audio_files


def find_maximum_number_of_audiofiles(paths):
    max_n = 0
    for path in paths:
        songs_number = len(get_all_audiofiles(path))
        if songs_number is None: 
            return None
        if songs_number > max_n: max_n = songs_number
    return max_n


def choose_random_songs(path, number):
    audio_files = get_all_audiofiles(path)
    chosen = random.sample(audio_files, number)
    return chosen


def get_random_times_for_sampling(length):
    timestamps = []
    for _ in range(0, 10):
        while True:
            sample_start_time = random.randrange(1, length)
            for timestamp in timestamps:
                t_difference = abs(timestamp - sample_start_time)
                if  t_difference < 7000:
                    break
            timestamps.append(sample_start_time)
            break
    return timestamps
