import os
import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from jdatetime import datetime as jdt
import cv2
import tkinter as tk
import time
from freshest_frame import FreshestFrame

parent_frame = None
middle_frame = None
cap = None
freshest_frame = None

def create_live_view_frame(parent):
    global parent_frame, middle_frame
    parent_frame = parent
    middle_frame = ttk.Frame(parent, padding="10", relief="solid")
    middle_label = ttk.Label(middle_frame, text="Live View", font=("Helvetica", 16))
    middle_label.pack(pady=10)
    
    return middle_frame

def set_camera(camera):
    global canvas
    global cap
    global camera_option
    global freshest_frame

    if cap is not None:
        cap.release()
    if freshest_frame is not None:
        freshest_frame.release()

    camera_option = camera
    rtsp_url = "rtsp://admin:Dailymilk10263@192.168.1.2:554/h264/ch9/main/av_stream"
    # Select the appropriate camera based on the camera_option
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG) if camera_option == "ip" else cv2.VideoCapture(0)
    freshest_frame = FreshestFrame(cap)
    print(camera_option)

def set_canvas(new_canvas):
    global canvas
    canvas = new_canvas

def start_stream():
    global canvas
    global camera_option
    global cap  # Declare cap as global
    global freshest_frame  # Declare cap as global
    global face_encodings
    global process_current_frame

    process_current_frame = True
    face_encodings = []

    if not cap.isOpened():
        print("Error: Cannot open selected camera stream")
        return
    
    last_saved_time = time.time()


    def update_frame():
        global  face_encodings, process_current_frame
        nonlocal last_saved_time
        face_locations = []
        face_names = []
        success, frame = freshest_frame.read()
        if not success:
            print("Error: Failed to retrieve frame")
            return

        if process_current_frame:
            # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # face_locations = face_recognition.face_locations(rgb_small_frame)
            # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # face_names = process_face_recognition(rgb_small_frame, face_encodings, face_locations)

        # if face_names and len(face_locations) > 0 and len(face_names) > 0 and len(face_locations)==len(face_names):
            # draw_faces(frame, face_locations, face_names)

        if canvas is not None:
            frame_pil = Image.fromarray(frame)
            frame_pil = frame_pil.resize((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            canvas.create_image(0, 0, anchor=tk.NW, image = frame_tk)
            canvas.image = frame_tk  # Keep a reference to avoid garbage collection
            # Increase the delay to reduce FPS
            canvas.after(50, update_frame)  # 50 ms delay corresponds to 20 FPS
        process_current_frame = not process_current_frame

    update_frame()

def stop_stream():
    global freshest_frame
    if freshest_frame is not None:
        freshest_frame.release()