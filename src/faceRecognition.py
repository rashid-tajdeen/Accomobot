import cv2
import face_recognition
import os
from pathlib import Path


class FaceRecognition:
    def __init__(self, known_faces_dir):
        self.known_faces = self._load_known_faces(known_faces_dir)
        self.video_capture = None

    def run(self):
        self._start_capturing()
        while True:
            # Capture each frame from the webcam
            ret, frame = self.video_capture.read()

            detected_location = self._detect_face(frame)
            if detected_location:
                frame = self._recognise_face(frame, detected_location)

            # Display the resulting frame
            cv2.imshow('Video Feed', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self._stop_capturing()

    def _load_known_faces(self, known_faces_dir):
        result = {}
        for file in os.listdir(known_faces_dir):
            if file.endswith(".jpg"):
                person = Path(file).stem
                result[person] = self._memorise_face(known_faces_dir + file)
        if result == {}:
            print("No faces to load")
            exit(0)
        else:
            return result

    @staticmethod
    def _memorise_face(image_path):
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        return encoding

    def _start_capturing(self):
        self.video_capture = cv2.VideoCapture(0)

    def _stop_capturing(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    @staticmethod
    def _rect_area(top, right, bottom, left):
        area = abs(top - bottom) * abs(left - right)
        return area

    @staticmethod
    def _draw_rectangle(frame, name, detected_location):
        (top, right, bottom, left) = detected_location
        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    def _detect_face(self, frame):
        # Find all face locations in the current frame
        detected_locations = face_recognition.face_locations(frame)

        dominant_location = None
        prev_bounding_area = 0
        # Loop through each face found in the frame
        for (top, right, bottom, left) in detected_locations:
            bounding_area = self._rect_area(top, right, bottom, left)
            if bounding_area > prev_bounding_area:
                dominant_location = (top, right, bottom, left)
                prev_bounding_area = bounding_area

        return dominant_location

    def _recognise_face(self, frame, detected_location):
        detected_encoding = face_recognition.face_encodings(frame, [detected_location])[0]

        name = "Unknown"
        # Loop through every known face
        for person, person_encoding in self.known_faces.items():
            is_known = face_recognition.compare_faces([person_encoding], detected_encoding)[0]
            if is_known:
                name = person
                break
        self._draw_rectangle(frame, name, detected_location)

        return frame
