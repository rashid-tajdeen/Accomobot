from qibullet import SimulationManager
from threading import Thread
import numpy as np
import time

from faceRecognition import FaceRecognition
from speechRecognition import SpeechRecognition
from bmlRealizer import BmlRealizer


class PepperRobot:
    def __init__(self):
        # Initialize the simulation environment
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

        self.faces_dir = "../known_faces/"
        self.talking_to = None
        self.fr = None
        self._start_face_recognition()

        self.sr = SpeechRecognition()

        self.bml = BmlRealizer(self.pepper)

    def _start_face_recognition(self):
        self.fr = FaceRecognition(self.faces_dir)
        Thread(target=self.fr.run).start()

    def _start_speech_recognition(self):
        self.sr = SpeechRecognition()
        Thread(target=self.sr.run).start()

    def wait_for_person(self):
        while True:
            person = self.fr.detected_person
            if person is not None:
                self.fr.stop_flag = True
                self._initiate_convo(person)
                break
            time.sleep(0.5)

    def _initiate_convo(self, person):
        self.talking_to = person
        if person == "Unknown":
            person = ""
        self.bml.greet(person)

    def respond(self):
        while True:
            listened_words = self.sr.listen()
            if listened_words != "":
                print(self.talking_to, ":", listened_words)
                self.bml.converse(listened_words)


if __name__ == "__main__":
    pepperRobot = PepperRobot()
    pepperRobot.wait_for_person()
    pepperRobot.respond()

