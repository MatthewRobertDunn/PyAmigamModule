import math
#Generates audio for a single channel
class channel:
    def __init__(self, samples, frame_rate_period):
        self.samples = samples
        self.frame_rate_period = frame_rate_period
        self.current_frame = 0
        self.sample = -1
        self.period = 0
    
    #plays a note using a given sample, at a frequency given by period, with given effect
    def play_note(self, sampleId, period, effect):
        if sampleId > -1: # start playing a brand new note
            self.current_frame = 0
            self.sample = self.samples[sampleId]
            self.period = period
            self.effect = effect
            self.frame_rate_scale = self.frame_rate_period / self.period
        else: 
            #only changing effect
            self.effect = effect
        return

    #returns audio frames for this channel for a given duration in secs.
    def get_frames(self, duration):
        requested_frames = math.floor(duration / self.frame_rate_period)

        buffer = [0.0] * requested_frames

        if self.sample is None:
            return     #nothing to play
        
        # we are not repeating and we finished playing this sample
        if self.sample.repeat_length == -1 & self.current_frame > self.sample.length:
            return buffer    #nothing to play
        
        
        #ignoring repeat for now
        for i in range(requested_frames):
            buffer[i] = self.sample.pcm_data[math.floor(self.current_frame)]
            self.current_frame += self.frame_rate_scale
            if self.current_frame > self.sample.length - 1:
                return buffer
        return buffer
