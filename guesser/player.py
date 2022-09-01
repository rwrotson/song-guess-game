from multiprocessing import Process
import magic
from pydub import AudioSegment
from pydub.playback import play


def get_song_object_from_path(path):
    file_format = magic.from_file(path, mime=True)
    if file_format == 'audio/mpeg':
        song = AudioSegment.from_mp3(path)
    elif file_format == 'audio/x-wav':
        song = AudioSegment.from_wav(path)
    elif file_format == 'audio/x-flac':
        song = AudioSegment.from_file(path, 'flac')
    return song


def get_samples_from_sample_times(path, list_of_start_times, length):
    song = get_song_object_from_path(path)
    samples_list = []
    for start in list_of_start_times:
        sample = song[start:start + length * 1000]
        samples_list.append(sample)
    return samples_list


def play_sample(sample):
    play(sample)


def play_song(song, start=0):
    if start == 0:
        process = Process(target=play, args=(song,))
    else:
        sample = song[start:]
        process = Process(target=play, args=(sample,))
    process.start()
    input('Press ENTER to stop.')
    process.terminate()
