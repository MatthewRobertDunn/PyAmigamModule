#Generates audio for a single channel
class Channel:
    def __init__(self, samples, time_step):
        self.samples = samples
        self.time_step = time_step
        self.current_time = 0
        self.sample = -1
        self.period = 0
    
    #plays a note using a given sample, at a frequency given by period, with given effect
    def play_note(self, sample, period, effect):
        if sample > -1: # start playing a brand new note
            self.current_time = 0
            self.sample = sample
            self.period = period
            self.effect = effect
        else: 
            #only changing effect
            self.effect = effect
        return

    #returns audio frames for this channel for a given duration in secs.
    def get_frames(self, duration):
        #todo        
        self.current_time += duration
        pass
