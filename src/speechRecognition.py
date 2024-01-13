import os
import sys
import time

from threading import Thread

import speech_recognition


class SpeechRecognition:
    def __init__(self):
        self.recogniser = speech_recognition.Recognizer()

    def listen(self):
        audio = self._listen_to_speech()
        text = self._speech_to_text(audio)
        return text

    def _listen_to_speech(self):
        with speech_recognition.Microphone() as source:
            print("Using system default Microphone...")
            self.recogniser.adjust_for_ambient_noise(source)
            audio = self.recogniser.listen(source)
            print("Listening...")
            return audio

    def _speech_to_text(self, audio):
        text = ""
        try:
            text = self.recogniser.recognize_google(audio)
        except speech_recognition.UnknownValueError:
            print("Sorry, could not understand audio.")
        except speech_recognition.RequestError as e:
            print(f"Request to Google Web Speech API failed; {e}")
        return text


if __name__ == "__main__":
    sr = SpeechRecognition()
    text = sr.listen()
    print(text)
