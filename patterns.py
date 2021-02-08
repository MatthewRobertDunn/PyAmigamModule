from struct import unpack_from

class Note:
    def __str__(self):
        return str(self.__dict__)

def get_pattern(buffer, pattern_number):
    return [get_pattern_row(buffer,pattern_number, row_number) for row_number in range(64)]

def get_pattern_row(buffer, pattern_number, row_number):
    return [get_pattern_note(buffer, pattern_number, row_number, channel_number) for channel_number in range(4)]

def get_pattern_note(buffer, pattern_number, row_number, channel_number):
    offset = 1084 + pattern_number * 1024 + row_number * 16 + channel_number * 4
    note = Note()
    raw = unpack_from('BBBB',buffer,offset)
    note.sample_number =  0b11110000 & raw[0] # top 4 bits sample number
    note.sample_number = note.sample_number + ((0b11110000 & raw[2]) >> 4) - 1 # lower 4 bits sample number, conver to 0 base
    assert(note.sample_number < 31)
    note.period = (0b00001111 & raw[0]) << 8 # top 4 bits of period
    note.period = note.period + raw[1] # lower 9 bits of period
    note.period = 1/3500000 * note.period # convert weird amiga periods to seconds
    note.effect = (0b00001111 & raw[2]) << 8 # top 4 bits of effect command
    note.effect = note.effect + raw[3] # lower 8 bits of effect command
    #todo unpack this mess
    return note
