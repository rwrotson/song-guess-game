from pathlib import Path
import music_tag

from guesser.player import (
    get_song_object_from_path, get_samples_from_sample_times
)
from guesser.utils import get_random_times_for_sampling


def handle_song(path, sample_duration):
    metadata = get_metadata_from_song_path(path)
    length = int(metadata['length'])
    song = get_song_object_from_path(path)
    samples_times = get_random_times_for_sampling(length)
    samples = get_samples_from_sample_times(path, samples_times, sample_duration)
    metadata['song_object'] = song
    metadata['sample_time'] = samples_times[0]
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
