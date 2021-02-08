import channel as Channel
class player:
    def __init__(self, samples,song, patterns, frame_rate_period):
        self.samples = samples
        self.patterns = patterns
        self.frame_rate_period = frame_rate_period
        self.channels = []
        self.channels.append(Channel.channel(samples,frame_rate_period))
        self.channels.append(Channel.channel(samples,frame_rate_period))
        self.channels.append(Channel.channel(samples,frame_rate_period))
        self.channels.append(Channel.channel(samples,frame_rate_period))
