from qibullet import SimulationManager
from threading import Thread
import numpy as np
import time

from faceRecognition import FaceRecognition
from speechRecognition import SpeechRecognition
from bmlRealizer import BmlRealizer
from rasaBot import MyRasa
from bayesian import MyBayesian
from constants import *


class PepperRobot:
    def __init__(self):
        # Initialize the simulation environment
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)

        self.myRasa = MyRasa()

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
        greet = self.myRasa.process("Hi")
        self._respond(greet)

    def keep_talking(self):
        count = 0
        while True:
            listened_words = self.sr.listen()
            if listened_words != "":
                print(self.talking_to, ":", listened_words)
                response = self.myRasa.process(listened_words)
                self._respond(response)
                count += 1
                if count == 9:
                    break
        self._ask_for_preferences()

    def _ask_for_preferences(self):
        parameters = {}
        parameters["rent_range"] = rent_range
        parameters["room_size"] = room_size
        parameters["property_type"] = property_type
        parameters["university"] = university
        result = []
        for att, value in parameters.items():
            print(f'\nEnter your preference for {att} from the options below :')
            for idx, val in enumerate(value):
                print(f'{idx + 1}. {val}')
            result.append(int(input("Please specify the index for the options above : ")))

        myBayesian = MyBayesian(result[0] - 1,
                                result[1] - 1,
                                result[2] - 1,
                                result[3] - 1)
        myBayesian.run()

    def _respond(self, response):
        self.bml.converse(response)


if __name__ == "__main__":
    pepperRobot = PepperRobot()
    pepperRobot.wait_for_person()
    pepperRobot.keep_talking()

