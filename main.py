import moduleloader
import sounddevice as sd
import player as Player
from multiprocessing import Process

def play_module():
    sd.default.samplerate = 44100
    sd.default.channels = 1
    sd.default.dtype = 'float32'
    current_time = 0
    time_step = 1.0 / sd.default.samplerate

    song = moduleloader.load("https://api.modarchive.org/downloads.php?moduleid=85375#an_adventurers_tale.mod")
    player = Player.Player(song,time_step)
    os = sd.OutputStream()
    os.start()

    while not player.finished:
        os.write(player.get_frames_row())

if __name__ == '__main__':
    p = Process(target=play_module)
    p.start()
    p.join()
    input("Press Enter to continue...")
