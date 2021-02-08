import requests 
import samples as Samples
import song
import patterns as Patterns
# https://www.ocf.berkeley.edu/~eek/index.html/tiny_examples/ptmod/ap12.html

response = requests.get("https://api.modarchive.org/downloads.php?moduleid=75502#popcorn_90.mod")
buffer = response.content

song_name = song.get_name(buffer)
print(song_name)

samples = [Samples.get_sample(buffer,x) for x in range(31)]
for sample in samples:
    print(sample)

song = song.get_song(buffer)
print(song)

patterns = [Patterns.get_pattern(buffer,pattern_number) for pattern_number in range(song.patterns_count)]
print(patterns[0][0][3])
print(f"Song has {len(patterns)} patterns")
print(f"Song is {song.length} sequences long")

Samples.get_pcm_data_for_samples(buffer,samples,song.patterns_count)

#print(list(samples[2].pcm_data))
import sounddevice as sd

sd.default.samplerate = 16000
sd.default.channels = 1
sd.default.dtype = 'float32'

def callback(outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = samples[0].pcm_data


with sd.OutputStream(callback=callback):
    sd.sleep(int(5 * 1000))


