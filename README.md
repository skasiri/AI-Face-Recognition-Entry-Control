# AI Face Recognition Entry System

This project is a complete AI-powered face recognition system with a GUI for tracking attendance. It uses the OpenCV and face_recognition libraries to detect and recognize faces, and stores the data in a SQLite database. The system has a user-friendly interface for adding new faces, tracking attendance, and managing subscriptions. The system also includes a live view feature that allows users to view the camera feed in real-time.

The project consists of the following components:

- A GUI built with tkinter for adding new faces, tracking attendance, and managing subscriptions
- A live view feature that displays the camera feed in real-time
- A database built with SQLite for storing face encodings and attendance data
- A face recognition system built with OpenCV and face_recognition for detecting and recognizing faces

The system is designed to be user-friendly and easy to use, with clear instructions and minimal setup required.

The face recognition system uses the face_recognition library, which is a simple and easy-to-use library based on the dlib library. It uses a convolutional neural network to detect and recognize faces, and is highly accurate and robust. The system supports face recognition on both still images and video streams.

The face_recognition library is available on the official website: https://github.com/ageitgey/face_recognition

### System Requirements

- Python version: 3.10.0

Ensure that you have Python 3.10.0 installed on your system. You can verify your Python version by running the following command:

```bash
python --version
```

If you do not have Python 3.10.0 installed, you can download it from the [official Python website](https://www.python.org/downloads/).

### Virtual Environment (venv)

A virtual environment is a self-contained directory that contains a Python interpreter and libraries. It is recommended to use a virtual environment to isolate your project's dependencies from the system Python environment.

To create a virtual environment, run the following command in your terminal:

```bash
python -m venv venv
```

Once the virtual environment is created, you can activate it by running the following command:

```bash
source venv/bin/activate
```

### Install requirements from requirements.txt

You can install all the requirements specified in the requirements.txt file using the following command:

```bash
pip install -r requirements.txt
```

This will install all the required packages and their dependencies.

### Run the Project

To run the project, execute the following command in your terminal:

```bash
python main.py
```
