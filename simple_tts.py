import warnings
warnings.filterwarnings("ignore")
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
# import librosa
from contextlib import redirect_stdout
import os
with open(os.devnull, 'w') as devnull:
    with redirect_stdout(devnull):
        tts = TTS(
            model_name="tts_models/en/ljspeech/vits",
            gpu=True
        )

text = "Welcome to Zork. You are standing in an open field west of a white house with a boarded front door."

import numpy as np
import sounddevice as sd

def change_speed_preserve_pitch(wav: np.ndarray, speed: float):
    """
    Speed up audio while approximately preserving pitch.
    Pure NumPy implementation.
    """

    # Step 1: Speed up by skipping samples
    indices = np.arange(0, len(wav), speed)
    sped = wav[indices.astype(int)]

    # Step 2: Resample back to original length
    target_len = int(len(sped) / speed)

    resampled = np.interp(
        np.linspace(0, len(sped), target_len),
        np.arange(len(sped)),
        sped
    )

    return resampled.astype(np.float32)


def speak(text: str, volume = 0.1):
    """
    Generate TTS for the given text and play it immediately.
    
    Args:
        text (str): The text to speak.
    """
    # Generate waveform as a numpy array
    if text:
        try:
            with open(os.devnull, 'w') as devnull:
                with redirect_stdout(devnull):
                    wav = tts.tts(text)
                    wav = np.array(wav, dtype=np.float32)

                    speed = 1.15  # 2x faster
                    indices = np.arange(0, len(wav), speed)
                    wav_fast = wav[indices.astype(int)]

                    sd.play(volume*wav_fast, samplerate=tts.synthesizer.output_sample_rate)
                    sd.wait()
        except IndexError:
            # print("NEXT ATTEMPT")
            speak(text)
        except UnicodeEncodeError:
            pass

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