
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
import librosa
import math
tts = TTS(
    model_name="tts_models/en/ljspeech/vits",
    gpu=True
)
import numpy as np
import sounddevice as sd
import librosa
from scipy.signal import resample
# from simple_tts_model import tts  # your TTS instance

def speak(text: str, speed: float = 1.5):
    """
    Play TTS faster while preserving pitch roughly using resampling.
    
    Args:
        text: string to speak
        speed: >1.0 = faster, <1.0 = slower
    """
    if not text:
        return

    try:
        wav = tts.tts(text)
        wav = np.asarray(wav, dtype=np.float32).flatten()
        sr = tts.synthesizer.output_sample_rate

        # Resample to adjust speed (naive)
        new_len = int(len(wav) / speed)
        wav_fast = resample(wav, new_len)

        # Play audio
        sd.play(wav_fast, samplerate=sr)
        sd.wait()

    except Exception as e:
        print(f"[TTS Error] {e}")


if __name__ == "__main__":
    ending = """Inside the Barrow
As you enter the barrow, the door closes inexorably behind you. Around you
it is dark, but ahead is an enormous cavern, brightly lit. Through its
center runs a wide stream. Spanning the stream is a small wooden
footbridge, and beyond a path leads into a dark tunnel. Above the bridge,
floating in the air, is a large sign. It reads:  All ye who stand before
this bridge have completed a great and perilous adventure which has tested
your wit and courage. You have mastered the first part of the ZORK trilogy.
Those who pass over this bridge must be prepared to undertake an even
greater adventure that will severely test your skill and bravery!

The ZORK trilogy continues with "ZORK II: The Wizard of Frobozz" and is
completed in "ZORK III: The Dungeon Master."
Your score is 350 (total of 350 points), in 280 moves.
This gives you the rank of Master Adventurer.

Would you like to restart the game from the beginning, restore a saved game
position, or end this session of the game?
(Type RESTART, RESTORE, or QUIT):"""
    speak(ending)