import math
import scipy
from scipy.signal import butter, lfilter

#Generates audio for a single channel
class channel:
    def __init__(self, samples, frame_rate_period):
        self.samples = samples
        self.frame_rate_period = frame_rate_period
        self.current_frame = 0
        self.sample = None
        self.period = 0
        self.nyquist_frequency = 0
        self.frame_rate = 1.0 / frame_rate_period
    
    #plays a note using a given sample, at a frequency given by period, with given effect
    def play_note(self, sampleId, period, effect):
        if sampleId > -1 and period > 0: # start playing a brand new note
            self.current_frame = 0
            self.sample = self.samples[sampleId]
            self.period = period
            self.nyquist_frequency = 1.0 / period / 2.0
            self.effect = effect
            self.frame_rate_scale = self.frame_rate_period / self.period
        else: 
            #only changing effect
            self.effect = effect
        return

    def get_frames(self, duration):
        frames = self.get_frames_raw(duration)
        if self.nyquist_frequency > 0:
            frames = butter_lowpass_filter(frames, self.nyquist_frequency, self.frame_rate)
        return frames

    #returns audio frames for this channel for a given duration in secs.
    def get_frames_raw(self, duration):
        requested_frames = math.floor(duration / self.frame_rate_period)
        buffer = [0.0] * requested_frames

        if self.sample is None:
            return buffer     #nothing to play
        
        # we are not repeating and we finished playing this sample
        if self.current_frame >= self.sample.length:
            return buffer    #nothing to play
        
        #ignoring repeat for now
        for i in range(requested_frames):
            buffer[i] = self.sample.pcm_data[math.floor(self.current_frame)]
            self.current_frame += self.frame_rate_scale
            if self.current_frame >= self.sample.length:
                return buffer
        return buffer

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
