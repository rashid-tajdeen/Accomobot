import speech_recognition


class SpeechRecognition:
    def __init__(self):
        self.recogniser = speech_recognition.Recognizer()
        self.audio = None
        self.text = None
        # Start service
        self.run()

    def run(self):
        self.connect_microphone()
        while True:
            self.listen_to_speech()
            self.print_text()

    def connect_microphone(self):
        with speech_recognition.Microphone() as source:
            print("Using system default Microphone...")
            self.recogniser.adjust_for_ambient_noise(source)  # Adjust for ambient noise

    def listen_to_speech(self):
        try:
            print("Listening...")
            # Using Google Web Speech API for recognition
            with speech_recognition.Microphone() as source:
                self.audio = self.recogniser.listen(source)
            self.text = self.recogniser.recognize_google(self.audio)
        except speech_recognition.UnknownValueError:
            print("Sorry, could not understand audio.")
        except speech_recognition.RequestError as e:
            print(f"Request to Google Web Speech API failed; {e}")

    def print_text(self):
        print(self.text)
        self.text = None


if __name__ == "__main__":
    SpeechRecognition()
