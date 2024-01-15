import math
import os
from time import sleep
from threading import Thread
import numpy as np
from random import uniform as rand

import xmltodict
import gtts
from playsound import playsound


class BmlRealizer:
    def __init__(self, pepper):
        self.bml_file = "bml.xml"
        self.audio_loc = "output.mp3"
        self._speaking = False
        self.pepper = pepper

    def __del__(self):
        if os.path.exists(self.audio_loc):
            os.remove(self.audio_loc)

    def greet(self, person=None):
        with open(self.bml_file) as fd:
            greet = xmltodict.parse(fd.read())["behaviours"]["greet"]
        if person:
            greet["speech"]["@text"] = "Hello " + person + ", how can I help you?"
        self._realize(greet)

    def nod_negative(self):
        with open(self.bml_file) as fd:
            nod_negative = xmltodict.parse(fd.read())["behaviours"]["nod_negative"]
        self._realize(nod_negative)

    def nod_positive(self):
        with open(self.bml_file) as fd:
            nod_positive = xmltodict.parse(fd.read())["behaviours"]["nod_positive"]
        self._realize(nod_positive)

    def happy_swirl(self):
        with open(self.bml_file) as fd:
            happy_swirl = xmltodict.parse(fd.read())["behaviours"]["happy_swirl"]
        self._realize(happy_swirl)

    def converse(self, text):
        with open(self.bml_file) as fd:
            converse = xmltodict.parse(fd.read())["behaviours"]["converse"]
        converse["speech"]["@text"] = text
        self._realize(converse)

    def _realize(self, bml):
        threads_list = []
        for behavior, attributes in bml.items():
            attributes = [attributes] if type(attributes) is not list else attributes
            for attribute in attributes:
                if behavior == "gesture" and attribute["@lexeme"] == "WAVE":
                    thrd = Thread(target=self._wave, args=[attribute])
                    threads_list.append(thrd)
                if behavior == "gesture" and attribute["@lexeme"] == "CONVERSE":
                    thrd = Thread(target=self._converse, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "speech":
                    self._speaking = True
                    thrd = Thread(target=self._speak, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "gaze":
                    thrd = Thread(target=self._gaze, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "head" and attribute["@lexeme"] == "NOD":
                    thrd = Thread(target=self._nod, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "posture" and attribute["@lexeme"] == "HAPPY_SWIRL":
                    Thread(target=self._swirl, args=[attribute]).start()

        # Start threads
        for thrd in threads_list:
            thrd.start()

        for thrd in threads_list:
            thrd.join()

    def _wave(self, attribute):
        l_hand = 1 if attribute["@mode"] == "LEFT_HAND" else 0
        r_hand = 1 if attribute["@mode"] == "RIGHT_HAND" else 0
        motion = {
            "RShoulderPitch": 0 * r_hand,
            "RShoulderRoll": -1.5 * r_hand,
            "RElbowYaw": 2 * r_hand,
            "RElbowRoll": 1.5 * r_hand,
            "LShoulderPitch": 0 * l_hand,
            "LShoulderRoll": 1.5 * l_hand,
            "LElbowYaw": -2 * l_hand,
            "LElbowRoll": -1.5 * l_hand,
        }

        start_time = int(attribute["@start"])
        duration = int(attribute["@end"]) - start_time

        # Wait until start time
        sleep(start_time)

        def move():
            # Set waving joint angles
            for key, value in motion.items():
                self.pepper.setAngles(key, value, 1.0)
        move()

        wave_count = 8.
        for i in range(int(wave_count)):
            if i % 2 == 0:
                motion["RElbowRoll"] = 1.5 * r_hand
                motion["LElbowRoll"] = 1.5 * l_hand
            else:
                motion["RElbowRoll"] = 0.5 * r_hand
                motion["LElbowRoll"] = 0.5 * l_hand
            move()
            sleep(duration / wave_count)

        # Reset the arm joint angles to their default positions
        for key in motion.keys():
            value = 0
            if key == "RShoulderPitch" or key == "LShoulderPitch":
                value = 1.5
            self.pepper.setAngles(key, value, 1.0)

    def _speak(self, attribute):
        # Wait until start time
        sleep(int(attribute["@start"]))

        # Convert text to speech using gTTS
        tts = gtts.gTTS(attribute["@text"])
        tts.save(self.audio_loc)  # Save the speech as an MP3 file
        playsound(self.audio_loc)
        self._speaking = False

    def _converse(self, attribute):
        # Wait until start time
        sleep(int(attribute["@start"]))

        constraints = {
            "RShoulderPitch": [0.75, 1.25],
            "RShoulderRoll": [-0.5, 0],
            "RElbowYaw": [1.5, 2],
            "RElbowRoll": [0.25, 0.75],
            "RWristYaw": [0.5, 1],
            "RHand": [1, 1],
            "LShoulderPitch": [0.75, 1.25],
            "LShoulderRoll": [0, 0.5],
            "LElbowYaw": [-2, -1.5],
            "LElbowRoll": [-0.75, 0.25],
            "LWristYaw": [-1, -0.5],
            "LHand": [1, 1]
        }

        # Make random hand movements
        while self._speaking:
            # Set random arm joint angles for talking
            for key, value in constraints.items():
                self.pepper.setAngles(key, rand(value[0], value[1]), 1.0)
            sleep(2)

        # Reset the arm joint angles to their default positions
        for key in constraints.keys():
            value = 0
            if key == "RShoulderPitch" or key == "LShoulderPitch":
                value = 1.5
            self.pepper.setAngles(key, value, 1.0)

    def _gaze(self, attribute):
        start_time = int(attribute["@start"])
        angle = math.radians(int(attribute["@angle"]))
        # Wait until start time
        sleep(start_time)
        # Making the robot gaze up towards the human's face
        self.pepper.setAngles("HeadPitch", angle, 1.0)

    def _nod(self, attribute):
        start_time = int(attribute["@start"])
        duration = int(attribute["@end"]) - start_time
        shake_count = int(attribute["@repetition"])
        delay = duration / (shake_count * 2)
        angle = math.radians(int(attribute["@angle"]))
        mode = "HeadPitch" if attribute["@mode"] == "POSITIVE" else "HeadYaw"

        # Wait until start time
        sleep(start_time)

        for i in range(shake_count):
            self.pepper.setAngles(mode, -angle, 1.0)
            sleep(delay)
            self.pepper.setAngles(mode, angle, 1.0)
            sleep(delay)

        self.pepper.setAngles(mode, 0.0, 1.0)

    def _swirl(self, attribute):
        # Wait until start time
        sleep(int(attribute["@start"]))

        # Open arms
        self.pepper.setAngles("RShoulderRoll", -np.pi / 2, 1.0)
        self.pepper.setAngles("LShoulderRoll", np.pi / 2, 1.0)
        self.pepper.setAngles("RElbowYaw", np.pi, 1.0)
        self.pepper.setAngles("LElbowYaw", -np.pi, 1.0)
        self.pepper.setAngles("RHand", np.pi / 2, 1.0)
        self.pepper.setAngles("LHand", np.pi / 2, 1.0)

        # Rotate the robot in place for a swirling motion
        self.pepper.move(0, 0, 6)  # Start rotation
        sleep(3)  # Rotate for 10 seconds
        self.pepper.move(0, 0, 0)  # Stop the rotation

        # Reset the robot's orientation
        self.pepper.move(0, 0, -6)  # Start rotation in the opposite direction
        sleep(3)  # Rotate for 10 seconds to return to original position
        self.pepper.move(0, 0, 0)  # Stop the rotation

        # Close arms
        self.pepper.setAngles("RShoulderRoll", 0, 1.0)
        self.pepper.setAngles("LShoulderRoll", 0, 1.0)
        self.pepper.setAngles("RElbowYaw", 0, 1.0)
        self.pepper.setAngles("LElbowYaw", 0, 1.0)
        self.pepper.setAngles("RHand", 0, 1.0)
        self.pepper.setAngles("LHand", 0, 1.0)
        sleep(1)
