import requests
import samples as Samples
import song as Song
import patterns as Patterns
import channel as Channel
import time
# https://www.ocf.berkeley.edu/~eek/index.html/tiny_examples/ptmod/ap12.html


def load(url):
    response = requests.get(url)
    buffer = response.content
    song_name = Song.get_name(buffer)
    samples = [Samples.get_sample(buffer, x) for x in range(31)]
    for sample in samples:
        print(sample)
    song = Song.get_song(buffer)
    song.samples = samples
    song.name = song_name
    print(song)
    patterns = [Patterns.get_pattern(buffer, pattern_number)
                for pattern_number in range(song.patterns_count)]
    song.patterns = patterns
    print(f"Song name is {song.name}")
    print(f"Song is {song.length} sequences long")
    print(f"Song has {len(song.patterns)} patterns")
    Samples.get_pcm_data_for_samples(buffer, samples, song.patterns_count)
    return song
