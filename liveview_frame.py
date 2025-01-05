import os
import datetime
import pickle
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from jdatetime import datetime as jdt
import cv2
import tkinter as tk
import time
from freshest_frame import FreshestFrame
import face_recognition
from utils.face_recognition import process_face_recognition
from utils.draw_face import draw_faces
from utils.encodings import save_encoding

parent_frame = None
middle_frame = None
cap = None
freshest_frame = None
camera_option = None
ip_camera_connection_string = ""
face_locations = []
face_names = []

if os.path.exists("config.pkl"):
    with open("config.pkl", "rb") as f:
        camera_option, ip_camera_connection_string = pickle.load(f)

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

    if camera is not None:
        camera_option = camera
    # Select the appropriate camera based on the camera_option
    if camera_option is not None:
        try:
            if camera_option == "ip":
                cap = cv2.VideoCapture(ip_camera_connection_string, cv2.CAP_FFMPEG)
            else:
                cap = cv2.VideoCapture(0)
            freshest_frame = FreshestFrame(cap)
            print(camera_option)
        except Exception as e:
            print(f"Error setting camera: {e}")

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

    if cap is None:
        print("Error: No camera selected")
        return

    if not cap.isOpened():
        print("Error: Cannot open selected camera stream")
        return
    
    last_saved_time = time.time()


    def update_frame():
        global  face_encodings, process_current_frame, face_names, face_locations
        nonlocal last_saved_time

        success, frame = freshest_frame.read()
        if not success:
            print("Error: Failed to retrieve frame")
            return

        if process_current_frame:
            # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = process_face_recognition(rgb_small_frame, face_encodings, face_locations)

        if face_names and len(face_locations) > 0 and len(face_names) > 0 and len(face_locations)==len(face_names):
            draw_faces(frame, face_locations, face_names)

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

def create_register_dialog(name, image_list):
    global parent_frame

    for item in image_list:
        if item[0] == name:
            name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
            # fname, face_image, confidence, landmarks_list, face_encoding  = item
            break
    
    def validate_form():
        if not entry_melli_code.get() or not entry_first_name.get() or not entry_last_name.get() or not entry_mobile.get():
            return False
        
        melli_code = entry_melli_code.get()
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM persons WHERE melli = ?', (melli_code,))
        if cursor.fetchone():
            messagebox.showerror("Error", "کد ملی تکراری است. لطفا کد ملی دیگری وارد کنید.")
            return False
        conn.close()

        try:
            melli_code = int(entry_melli_code.get())
        except ValueError:
            messagebox.showerror("Error", "کد ملی باید عدد باشد.")
            return False
        
        if len(str(melli_code)) != 10:
            messagebox.showerror("Error", "کد ملی باید 10 رقم باشد.")
            return False
        
        check = sum([int(str(melli_code)[i]) * (10 - i) for i in range(9)]) % 11
        if (check < 2 and int(str(melli_code)[-1]) != check) or (check >= 2 and int(str(melli_code)[-1]) != 11 - check):
            messagebox.showerror("Error", "کد ملی نامعتبر است. لطفا بررسی کنید.")
            return False

        return True

    def register_user():
        if not validate_form():
            return
        melli_code = entry_melli_code.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        mobile = entry_mobile.get()
        save_encoding(name, face_encoding, melli_code, first_name, last_name, mobile)
        # Here you can add the code to handle the registration logic
        messagebox.showinfo("Registration", "User registered successfully!")
        cancel_registration()

    def cancel_registration():
        global parent_frame
        middle_frame.pack_forget()
        middle_frame.grid_remove()
        canvas = create_live_view_frame(parent_frame)
        set_canvas(canvas)
        canvas.pack(fill="both")

    middle_frame.pack_forget()
    middle_frame.grid_remove()

    register_frame = ttk.Frame(parent_frame, padding="10", relief="solid")
    register_frame.grid(row=0, column=1, sticky="nsew")

    middle_label = ttk.Label(register_frame, text="تعریف شخص جدید", font=("Helvetica", 16))
    middle_label.grid(row=0, column=1, padx=10, pady=5)

    # Display the face image
    image_size = (120, 120)
    image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
    image = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image)
    
    image_label = ttk.Label(register_frame, image=photo)
    image_label.image = photo
    image_label.grid(row=0, column=0, padx=10, pady=5)
   
    # Melli Code
    tk.Label(register_frame, text="کد ملی").grid(row=1, column=1, padx=10, pady=5)
    entry_melli_code = tk.Entry(register_frame)
    entry_melli_code.insert(0, "")
    entry_melli_code.grid(row=1, column=0, padx=10, pady=5)

    # First Name
    tk.Label(register_frame, text="نام").grid(row=2, column=1, padx=10, pady=5)
    entry_first_name = tk.Entry(register_frame)
    entry_first_name.insert(0, "")
    entry_first_name.grid(row=2, column=0, padx=10, pady=5)

    # Last Name
    tk.Label(register_frame, text="نام خانوادگی").grid(row=3, column=1, padx=10, pady=5)
    entry_last_name = tk.Entry(register_frame)
    entry_last_name.insert(0, "")
    entry_last_name.grid(row=3, column=0, padx=10, pady=5)

    # Mobile
    tk.Label(register_frame, text="تلفن همراه").grid(row=4, column=1, padx=10, pady=5)
    entry_mobile = tk.Entry(register_frame)
    entry_mobile.insert(0, "")
    entry_mobile.grid(row=4, column=0, padx=10, pady=5)

    # Apply Button
    apply_button = tk.Button(register_frame, text="ذخیره", command=register_user, bg="green", fg="white", height=2)
    apply_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    # Cancel Button
    cancel_button = tk.Button(register_frame, text="لغو", command=cancel_registration, bg="red", fg="white", height=2)
    cancel_button.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
