import math
import os
from time import sleep
from threading import Thread

import xmltodict
import gtts
from playsound import playsound


class BmlRealizer:
    def __init__(self, pepper):
        self.bml_file = "bml.xml"
        self.audio_loc = "output.mp3"
        self.pepper = pepper

    def __del__(self):
        if os.path.exists(self.audio_loc):
            os.remove(self.audio_loc)

    def greet(self, person=None):
        with open(self.bml_file) as fd:
            greet = xmltodict.parse(fd.read())["behaviours"]["greet"]
        if person:
            greet["speech"]["@text"] = "Hello " + person + ", how can I help you?"

        print(greet)
        self._realize(greet)

    def _realize(self, bml):
        threads_list = []
        for behavior, attributes in bml.items():
            attributes = [attributes] if type(attributes) is not list else attributes
            for attribute in attributes:
                if behavior == "gesture" and attribute["@lexeme"] == "WAVE":
                    thrd = Thread(target=self._wave, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "speech":
                    thrd = Thread(target=self._speak, args=[attribute])
                    threads_list.append(thrd)
                elif behavior == "gaze":
                    thrd = Thread(target=self._gaze, args=[attribute])
                    threads_list.append(thrd)
                # elif behavior == "head" and attributes["lexeme"] == "NOD":
                #     Thread(target=self.nod).start()
                # elif behavior == "posture" and attributes["lexeme"] == "HAPPY_SWIRL":
                #     Thread(target=self.happy_swirl).start()

        # Start threads
        for thrd in threads_list:
            thrd.start()

        for thrd in threads_list:
            thrd.join()

    def _wave(self, attributes):
        r_l = 0 if attributes["@mode"] == "RIGHT_HAND" else 1
        multiplier = 1 if attributes["@mode"] == "RIGHT_HAND" else -1

        ShoulderPitch = ["RShoulderPitch", "LShoulderPitch"]
        ShoulderRoll = ["RShoulderRoll", "LShoulderRoll"]
        ElbowYaw = ["RElbowYaw", "LElbowYaw"]
        ElbowRoll = ["RElbowRoll", "LElbowRoll"]

        start_time = int(attributes["@start"])
        duration = int(attributes["@end"]) - start_time

        # Wait until start time
        sleep(start_time)

        # Set the arm joint angles for waving
        self.pepper.setAngles(ShoulderPitch[r_l], 0, 1.0)
        self.pepper.setAngles(ShoulderRoll[r_l], -1.5 * multiplier, 1.0)
        self.pepper.setAngles(ElbowYaw[r_l], 2 * multiplier, 1.0)

        wave_count = 8.
        for i in range(int(wave_count)):
            if i % 2 == 0:
                self.pepper.setAngles(ElbowRoll[r_l], 1.5 * multiplier, 1.0)
            else:
                self.pepper.setAngles(ElbowRoll[r_l], 0.5 * multiplier, 1.0)
            sleep(duration / wave_count)

        # Reset the arm joint angles to their default positions
        self.pepper.setAngles(ShoulderPitch[r_l], 0.0, 1.0)
        self.pepper.setAngles(ShoulderRoll[r_l], 0.0, 1.0)
        self.pepper.setAngles(ElbowYaw[r_l], 0.0, 1.0)
        self.pepper.setAngles(ElbowRoll[r_l], 0.0, 1.0)

    def _speak(self, attributes):
        # Wait until start time
        sleep(int(attributes["@start"]))

        # Convert text to speech using gTTS
        tts = gtts.gTTS(attributes["@text"])
        tts.save(self.audio_loc)  # Save the speech as an MP3 file
        playsound(self.audio_loc)

    def _gaze(self, attributes):
        start_time = int(attributes["@start"])
        duration = int(attributes["@end"]) - start_time

        angle = math.radians(int(attributes["@angle"]))

        # Wait until start time
        sleep(start_time)

        # Making the robot gaze up towards the human's face
        self.pepper.setAngles("HeadPitch", angle, 1.0)
        sleep(duration)

        # Reset gaze
        self.pepper.setAngles("HeadPitch", 0.0, 1.0)
    #
    # def nod(self):
    #     # Make the robot nod twice
    #     self.pepper.setAngles("HeadPitch", -0.2, 1.0)
    #     time.sleep(0.5)
    #     self.pepper.setAngles("HeadPitch", 0.2, 1.0)
    #     time.sleep(0.5)
    #     self.pepper.setAngles("HeadPitch", -0.2, 1.0)
    #     time.sleep(0.5)
    #     self.pepper.setAngles("HeadPitch", 0.2, 1.0)
    #     time.sleep(0.5)
    #     self.pepper.setAngles("HeadPitch", 0.0, 1.0)
    #
    # def happy_swirl(self):
    #
    #     # Open arms
    #     self.pepper.setAngles("RShoulderRoll", -np.pi / 2, 1.0)
    #     self.pepper.setAngles("LShoulderRoll", np.pi / 2, 1.0)
    #     self.pepper.setAngles("RElbowYaw", np.pi, 1.0)
    #     self.pepper.setAngles("LElbowYaw", -np.pi, 1.0)
    #     self.pepper.setAngles("RHand", np.pi / 2, 1.0)
    #     self.pepper.setAngles("LHand", np.pi / 2, 1.0)
    #
    #     # Rotate the robot in place for a swirling motion
    #     self.pepper.move(0, 0, 6)  # Start rotation
    #     time.sleep(3)  # Rotate for 10 seconds
    #     self.pepper.move(0, 0, 0)  # Stop the rotation
    #
    #     # Reset the robot's orientation
    #     self.pepper.move(0, 0, -6)  # Start rotation in the opposite direction
    #     time.sleep(3)  # Rotate for 10 seconds to return to original position
    #     self.pepper.move(0, 0, 0)  # Stop the rotation
    #
    #     # Close arms
    #     self.pepper.setAngles("RShoulderRoll", 0, 1.0)
    #     self.pepper.setAngles("LShoulderRoll", 0, 1.0)
    #     self.pepper.setAngles("RElbowYaw", 0, 1.0)
    #     self.pepper.setAngles("LElbowYaw", 0, 1.0)
    #     self.pepper.setAngles("RHand", 0, 1.0)
    #     self.pepper.setAngles("LHand", 0, 1.0)
    #
    #     time.sleep(1)
