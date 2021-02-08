from math import trunc
import requests 
import samples as Samples
import song
import patterns as Patterns
import channel as Channel
import time
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

sd.default.samplerate = 44100
sd.default.channels = 1
sd.default.dtype = 'float32'

current_time = 0
time_step = 1.0 / sd.default.samplerate


channel = Channel.channel(samples,time_step)

note = patterns[0][4][0]

channel.play_note(note.sample_number,note.period,note.effect) #play note using sample 0, 1/16000th period, 0 effect
buffer = channel.get_frames(1) # get 1 second worth of frames
sd.play(buffer, blocking=True) #play the buffer

channel.play_note(1,1/30100,0) #play note using sample 0, 1/16000th period, 0 effect
buffer = channel.get_frames(1) # get 1 second worth of frames
sd.play(buffer, blocking=True) #play the buffer

t = time.perf_counter()
channel.play_note(2,1/22000,0) #play note using sample 0, 1/16000th period, 0 effect
buffer = channel.get_frames(1) # get 1 second worth of frames
elapsed_time = time.perf_counter() - t
print(f"producing 1 second of audio took {elapsed_time}")
sd.play(buffer, blocking=True) #play the buffer

time.sleep(1)
#def callback(outdata, frames, time, status):
#    if status:
#        print(status)
#    outdata[:] = samples[0].pcm_data


#with sd.OutputStream(callback=callback):
#    sd.sleep(int(5 * 1000))
