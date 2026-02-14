import sounddevice as sd
import soundfile as sf
import numpy as np

# duration = 3  # seconds
# sr = 16000    # sample rate
# # print(sd.query_devices())  # check device names and indices
# audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, device=3)

# print("Recording for 3 seconds...")
# # audio = sd.rec(int(duration * sr), samplerate=sr, channels=1)
# sd.wait()

# audio = audio.flatten()
# print("Min:", audio.min(), "Max:", audio.max())
# print("Mean:", audio.mean())
# print("Non-zero samples:", np.count_nonzero(audio))
from pathlib import Path
HERE = Path(__file__).parent
STATIC = HERE / "static"
BELL = STATIC / "bell_02.ogg"
GONG = STATIC / "gong_01.ogg"
data, samplerate = sf.read(GONG)
print(data, samplerate)
sd.play(0.1*data, samplerate)
sd.wait() 