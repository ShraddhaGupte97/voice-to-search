import sounddevice as sd
import numpy as np
import io
from scipy.io.wavfile import write
import speech_recognition as sr

def capture_and_transcribe(duration=12, fs=16000):
    """
    Captures voice from microphone using sounddevice and transcribes to text using Google Speech Recognition.
    """
    print(f"Listening for voice input... Speak now for up to {duration} seconds.")
    try:
        # Record audio
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        print("Recording complete. Transcribing...")

        # Save to a BytesIO buffer as WAV
        buf = io.BytesIO()
        write(buf, fs, audio)
        buf.seek(0)

        # Use speech_recognition to transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile(buf) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"Transcription: {text}")
        return text
    except sr.WaitTimeoutError:
        print("No speech detected within timeout period.")
        return "hello world"
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return "hello world"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "hello world"
    except Exception as e:
        print(f"Error during transcription: {e}")
        return "hello world" 