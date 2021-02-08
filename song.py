from struct import unpack_from

class Song:
    def __str__(self):
        return str(self.__dict__)


def get_name(buffer):
    return  b''.join(unpack_from('ssssssssssssssssssss',buffer,0)).strip(b'\x00')

def get_song(buffer):
    song = Song()
    song.length = unpack_from('BB',buffer, 950)[0]
    assert(song.length <= 128)
    song.positions = unpack_from('B'*128,buffer,952)       #which pattern to play at what 'position'
    song.file_type = b''.join(unpack_from('cccc',buffer,1080))
    assert(song.file_type == b'M.K.')
    song.patterns_count = max(song.positions) + 1
    return song
