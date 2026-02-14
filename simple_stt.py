import torch
import whisper
import numpy as np
import sounddevice as sd
model = whisper.load_model("small", device="cuda")

def transcribe(duration=3, sr=16000):
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, device=3)
    sd.wait()
    audio = audio.flatten().astype(np.float32)
    result = model.transcribe(audio)
    # print(audio.min(), audio.max())
    return result["text"]

def zork_test():
    while True:
        print("Testing")
        result = transcribe(duration=1)
        print(result)
        if result in [" Zork.", " ZOR", " Zork!", " Thank you.", "Clique.", " work."]:
            print("HERE")
            try:
                the_text = transcribe(duration=2)
                return the_text
            except IndexError:
                pass
if __name__ == "__main__":
    print(zork_test())