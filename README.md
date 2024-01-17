# HCIR_Project
An interactive robot to assist incoming students find accommodation based on their preferences.

## Getting Started

### Cloning the repository

Clone the repository using

```shell
git clone https://github.com/rashid-tajdeen/HCIR_Project.git
cd HCIR_Project
```

### Setting up the environment

Have virtualenv installed using
```shell
sudo apt install python3.8-venv
```

Create a virtual env using
```shell
python3.8 -m venv venv
```

Activate the virtual environment
```shell
source venv/bin/activate
```

Install the requirements using
```shell
pip install -r requirements.txt
```

If an error is thrown for building wheel for pyaudio, try the below line
and rerun installing requirements
```shell
sudo apt-get install portaudio19-dev
```

## Running modules

### Face Recognition

- Place a picture of yourself in the _known_faces_ directory with your name.
  For example, _rashid.jpg_
- From inside the source directory
```shell
cd src
```
- Run the module using the command
```shell
python3 faceRecognition.py
```
- A window pops up with the video stream and a labeled face.

### Speech Recognition

- From inside the source directory
```shell
cd src
```
- Run the module using the command
```shell
python3 speechRecognition.py
```
- Your speech will be printed on the console

### Speech Recognition

#### Installing Rasa

```shell
pip3 install --upgrade pip
pip3 install rasa==3.6.15
```

#### Training Rasa

```shell
cd src/rasa
python3.8 -m rasa train
```

## Usage

Run the application using

```shell
cd src
python3 pepper.py
```
