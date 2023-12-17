from faceRecognition import FaceRecognition


def main():
    faces_dir = "../known_faces/"
    recogniser = FaceRecognition(faces_dir)
    recogniser.run()


if __name__ == '__main__':
    main()
