import os
from qibullet import SimulationManager
import gtts
from playsound import playsound
from threading import Thread
import numpy as np
import time

from faceRecognition import FaceRecognition
from speechRecognition import SpeechRecognition


class PepperRobot:
    def __init__(self):
        # Initialize the simulation environment
        # Loading Robot and  Ground
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
        self.audio_loc = "output.mp3"

        self.faces_dir = "../known_faces/"
        self.talking_to = None
        self.fr = None
        self._start_face_recognition()

        self.sr = SpeechRecognition()

    def __del__(self):
        if os.path.exists(self.audio_loc):
            os.remove(self.audio_loc)

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
        welcome_message = "Hello " + person + ", how can I help you?"
        self.speak(welcome_message)

    def respond(self):
        while True:
            listened_words = self.sr.listen()
            if listened_words != "":
                print(self.talking_to, ":", listened_words)

    def speak(self, text, thread_mode=False):
        # Convert text to speech using gTTS
        tts = gtts.gTTS(text)
        tts.save(self.audio_loc)  # Save the speech as an MP3 file

        def play_speech():
            playsound(self.audio_loc)

        if thread_mode:
            # Play the speech using the playsound library in a separate thread
            Thread(target=play_speech).start()
        else:
            play_speech()

    def wave(self):
        # Set the arm joint angles for waving
        self.pepper.setAngles("LShoulderPitch", -1.0, 1.0)
        self.pepper.setAngles("LShoulderRoll", 0.5, 1.0)
        self.pepper.setAngles("LElbowYaw", -0.5, 1.0)
        self.pepper.setAngles("LElbowRoll", -1.0, 1.0)

        # Wait for a few seconds to maintain the waving gesture
        time.sleep(2)

        # Reset the arm joint angles to their default positions
        self.pepper.setAngles("LShoulderPitch", 0.0, 1.0)
        self.pepper.setAngles("LShoulderRoll", 0.0, 1.0)
        self.pepper.setAngles("LElbowYaw", 0.0, 1.0)
        self.pepper.setAngles("LElbowRoll", 0.0, 1.0)

    def gaze(self):
        # Making the robot gaze up towards the human's face
        self.pepper.setAngles("HeadPitch", -0.2, 1.0)
        time.sleep(3)
        # Reset gaze
        self.pepper.setAngles("HeadPitch", 0.0, 1.0)

    def nod(self):
        # Make the robot nod twice
        self.pepper.setAngles("HeadPitch", -0.2, 1.0)
        time.sleep(0.5)
        self.pepper.setAngles("HeadPitch", 0.2, 1.0)
        time.sleep(0.5)
        self.pepper.setAngles("HeadPitch", -0.2, 1.0)
        time.sleep(0.5)
        self.pepper.setAngles("HeadPitch", 0.2, 1.0)
        time.sleep(0.5)
        self.pepper.setAngles("HeadPitch", 0.0, 1.0)

    def happy_swirl(self):

        # Open arms
        self.pepper.setAngles("RShoulderRoll", -np.pi / 2, 1.0)
        self.pepper.setAngles("LShoulderRoll", np.pi / 2, 1.0)
        self.pepper.setAngles("RElbowYaw", np.pi, 1.0)
        self.pepper.setAngles("LElbowYaw", -np.pi, 1.0)
        self.pepper.setAngles("RHand", np.pi / 2, 1.0)
        self.pepper.setAngles("LHand", np.pi / 2, 1.0)

        # Rotate the robot in place for a swirling motion
        self.pepper.move(0, 0, 6)  # Start rotation
        time.sleep(3)  # Rotate for 10 seconds
        self.pepper.move(0, 0, 0)  # Stop the rotation

        # Reset the robot's orientation
        self.pepper.move(0, 0, -6)  # Start rotation in the opposite direction
        time.sleep(3)  # Rotate for 10 seconds to return to original position
        self.pepper.move(0, 0, 0)  # Stop the rotation

        # Close arms
        self.pepper.setAngles("RShoulderRoll", 0, 1.0)
        self.pepper.setAngles("LShoulderRoll", 0, 1.0)
        self.pepper.setAngles("RElbowYaw", 0, 1.0)
        self.pepper.setAngles("LElbowYaw", 0, 1.0)
        self.pepper.setAngles("RHand", 0, 1.0)
        self.pepper.setAngles("LHand", 0, 1.0)

        time.sleep(1)


if __name__ == "__main__":
    pepperRobot = PepperRobot()
    pepperRobot.wait_for_person()
    pepperRobot.respond()

