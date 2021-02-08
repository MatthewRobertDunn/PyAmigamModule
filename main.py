import moduleloader
import sounddevice as sd
import time
import channel as Channel
import player as Player

sd.default.samplerate = 44100
sd.default.channels = 1
sd.default.dtype = 'float32'

current_time = 0
time_step = 1.0 / sd.default.samplerate

song = moduleloader.load("https://api.modarchive.org/downloads.php?moduleid=75502#popcorn_90.mod")

player = Player.Player(song,time_step)

os = sd.OutputStream()
os.start()

while not player.finished:
    os.write(player.get_frames_row())

input("Press Enter to continue...")
