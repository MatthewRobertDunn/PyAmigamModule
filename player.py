import channel as Channel
import math
import numpy as np
class Player:
    def __init__(self, song, frame_rate_period):
        self.song = song
        self.frame_rate_period = frame_rate_period
        self.channels = []
        self.sequence = 0
        self.channels.append(Channel.channel(song.samples,frame_rate_period))
        self.channels.append(Channel.channel(song.samples,frame_rate_period))
        self.channels.append(Channel.channel(song.samples,frame_rate_period))
        self.channels.append(Channel.channel(song.samples,frame_rate_period))
        self.sequence = 0
        self.pattern_row = 0
        self.last_note_counter = 0
        self.finished = False

    def get_frames(self, duration):
        requested_frames = math.floor(duration / self.frame_rate_period)
        buffer = [0.0] * requested_frames



    def get_frames_row(self):
        self.play_notes(self.song.sequences[self.sequence],self.pattern_row)
        self.pattern_row += 1
        if self.pattern_row > 63:
            self.sequence += 1
            self.pattern_row = 0
            print(f"squence {self.sequence} pattern {self.song.sequences[self.sequence]}")
            if self.sequence >= self.song.length:
                self.finished = True
                print("Finished!")


        notes = [x.get_frames(self.song.note_period) for x in self.channels ]
        mix = np.add.reduce(np.single(notes)) * 0.25
        return mix


    def play_notes(self, pattern, row):
        for i, channel in enumerate(self.channels):
            note = self.song.patterns[pattern][row][i]
            print(f"{note.sample_number:03}", end=" ")
            channel.play_note(note.sample_number,note.period,note.effect)
        print("")
