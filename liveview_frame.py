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
from utils.encodings import save_encoding, update_person, delete_person, get_person_by_melli
from utils.subscription import Subscription

parent_frame = None
middle_frame = None
cap = None
freshest_frame = None
camera_option = None
ip_camera_connection_string = ""
face_locations = []
face_names = []
on_air = False
frame_size_ratio = 0.5

if os.path.exists("config.pkl"):
    with open("config.pkl", "rb") as f:
        camera_option, ip_camera_connection_string = pickle.load(f)

def create_live_view_frame(parent):
    global parent_frame, middle_frame, canvas
    parent_frame = parent
    middle_frame = ttk.Frame(parent, padding="10", relief="solid")
    middle_frame.grid(row=0, column=1, sticky="nsew")

    middle_label = ttk.Label(middle_frame, text="Live View", font=("Helvetica", 16))
    middle_label.pack(pady=10)
    canvas = tk.Canvas(middle_frame, width=640, height=480)
    
    return canvas

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
            cap = None
            freshest_frame = None
            canvas.delete("all")
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
        global canvas, on_air
        global  face_encodings, process_current_frame, face_names, face_locations
        nonlocal last_saved_time

        success, frame = freshest_frame.read()
        if not success:
            on_air = False
            print("Error: Failed to retrieve frame")
            return

        if process_current_frame:
            on_air = True
            small_frame = cv2.resize(frame, (0, 0), fx=frame_size_ratio, fy=frame_size_ratio)
            gray_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(gray_small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = process_face_recognition(rgb_small_frame, face_encodings, face_locations)

        if face_names and len(face_locations) > 0 and len(face_names) > 0 and len(face_locations)==len(face_names):
            draw_faces(frame, face_locations, face_names, frame_size_ratio)

        if canvas is not None:
            frame_pil = Image.fromarray(frame)
            frame_pil = frame_pil.resize((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            canvas.create_image(0, 0, anchor=tk.NW, image = frame_tk)
            canvas.image = frame_tk  # Keep a reference to avoid garbage collection
            # Increase the delay to reduce FPS
            canvas.after(100, update_frame)  # 100 ms delay corresponds to 10 FPS
        process_current_frame = not process_current_frame

    update_frame()

def stop_stream():
    global freshest_frame, on_air
    on_air = False
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
        global parent_frame, canvas, middle_frame
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

def create_edit_dialog(melli, image_list):
    global parent_frame

    person = get_person_by_melli(melli)

    if person is None:
        return
    
    for item in image_list: 
        if item[0] == melli:
            melli, name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item 
            break

    def validate_form():
        if not entry_first_name.get() or not entry_last_name.get() or not entry_mobile.get():
            return False

        return True

    def update_user():
        if not validate_form():
            return
        melli_code = entry_melli_code.get()
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        mobile = entry_mobile.get()
        update_person(melli_code, first_name, last_name, mobile)
        # Here you can add the code to handle the registration logic
        messagebox.showinfo("Update User Info", "User updated successfully!")
        cancel_registration()

    def cancel_registration():
        global parent_frame
        middle_frame.pack_forget()
        middle_frame.grid_remove()
        canvas = create_live_view_frame(parent_frame)
        set_canvas(canvas)
        canvas.pack(fill="both")

    def delete_user():
        if messagebox.askyesno("Verify Delete", "Are you sure you want to delete this user?"):
            delete_person(melli)
            messagebox.showinfo("Delete User", "User deleted successfully!")
        cancel_registration()

    middle_frame.pack_forget()
    middle_frame.grid_remove()

    register_frame = ttk.Frame(parent_frame, padding="10", relief="solid")
    register_frame.grid(row=0, column=1, sticky="nsew")

    middle_label = ttk.Label(register_frame, text="ویرایش شخص", font=("Helvetica", 16))
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
    entry_melli_code.insert(0, melli)
    entry_melli_code.configure(state='readonly')
    entry_melli_code.grid(row=1, column=0, padx=10, pady=5)

    # First Name
    tk.Label(register_frame, text="نام").grid(row=2, column=1, padx=10, pady=5)
    entry_first_name = tk.Entry(register_frame)
    entry_first_name.insert(0, person[2])
    entry_first_name.grid(row=2, column=0, padx=10, pady=5)

    # Last Name
    tk.Label(register_frame, text="نام خانوادگی").grid(row=3, column=1, padx=10, pady=5)
    entry_last_name = tk.Entry(register_frame)
    entry_last_name.insert(0, person[3])
    entry_last_name.grid(row=3, column=0, padx=10, pady=5)

    # Mobile
    tk.Label(register_frame, text="تلفن همراه").grid(row=4, column=1, padx=10, pady=5)
    entry_mobile = tk.Entry(register_frame)
    entry_mobile.insert(0, person[4])
    entry_mobile.grid(row=4, column=0, padx=10, pady=5)

    # Delete Button
    delete_button = tk.Button(register_frame, text="حذف", command=delete_user, bg="red", fg="white", height=2)
    delete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Apply Button
    apply_button = tk.Button(register_frame, text="ذخیره", command=update_user, bg="green", fg="white", height=2)
    apply_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    # Cancel Button
    cancel_button = tk.Button(register_frame, text="لغو", command=cancel_registration, bg="red", fg="white", height=2)
    cancel_button.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

def create_subscribe_form(melli):
    global parent_frame

    print('create_subscribe_form for: ', melli)

    person = get_person_by_melli(melli)

    if person is None:
        return
    
    sub = Subscription()
    active = sub.get_active_subscription(melli)
    color = "green" if active else "yellow"

    start_date = jdt.now().strftime("%Y-%m-%d")
    end_date = jdt.now().date() + datetime.timedelta(days=30)
    end_date = end_date.strftime("%Y-%m-%d")
    num_of_sessions = 26
    remaining_sessions = 26

    if active is not None:
        start_date = jdt.fromgregorian(date=jdt.strptime(active[2], "%Y-%m-%d")).strftime("%Y-%m-%d")
        end_date = jdt.fromgregorian(date=jdt.strptime(active[3], "%Y-%m-%d")).strftime("%Y-%m-%d")
        num_of_sessions = active[4]
        remaining_sessions = active[5]

    def validate_form():
        if not entry_start_date.get() or not entry_end_date.get() or not entry_num_sessions.get() or not entry_remaining_sessions.get():
            messagebox.showerror("Error", "All fields are required.")
            return False
        
        start_date_jalali = entry_start_date.get()
        start_date_parts = start_date_jalali.split('-')
        start_date_gregorian = jdt(
            int(start_date_parts[0]), int(start_date_parts[1]), int(start_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")

        end_date_jalali = entry_end_date.get()
        end_date_parts = end_date_jalali.split('-')
        end_date_gregorian = jdt(
            int(end_date_parts[0]), int(end_date_parts[1]), int(end_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")

        if start_date_gregorian > end_date_gregorian:
            messagebox.showerror("Error", "Start date must be before end date.")
            return False
        
        try:
            num_of_sessions = int(entry_num_sessions.get())
            remaining_sessions = int(entry_remaining_sessions.get())
        except ValueError:
            messagebox.showerror("Error", "Number of sessions and remaining sessions must be integers.")
            return False
        
        if num_of_sessions <= 0 or remaining_sessions <= 0:
            messagebox.showerror("Error", "Number of sessions and remaining sessions must be greater than 0.")
            return False
        
        if num_of_sessions < remaining_sessions:
            messagebox.showerror("Error", "Number of sessions must be greater than or equal to remaining sessions.")
            return False
        
        return True

    def save_subscription():
        if not validate_form():
            return
        sub = Subscription()
        sub.add_subscription(person[1], entry_start_date.get(), entry_end_date.get(), entry_num_sessions.get(), entry_remaining_sessions.get())
        cancel_subscription()

    def delete_subscription():
        if messagebox.askyesno("Verify Delete", "Are you sure you want to delete this subscription?"):
            sub = Subscription()
            sub.delete_subscription(active[0])
        cancel_subscription()

    def update_subscription():
        if not validate_form():
            return
        sub = Subscription()
        sub.update_subscription(active[0], entry_start_date.get(), entry_end_date.get(), entry_num_sessions.get(), entry_remaining_sessions.get())
        cancel_subscription()

    def cancel_subscription():
        global parent_frame
        middle_frame.pack_forget()
        middle_frame.grid_remove()
        canvas = create_live_view_frame(parent_frame)
        set_canvas(canvas)
        canvas.pack(fill="both")
        
    middle_frame.pack_forget()
    middle_frame.grid_remove()

    subscribe_frame = ttk.Frame(parent_frame, padding="10", relief="solid")
    subscribe_frame.grid(row=0, column=1, sticky="nsew")

    title = 'افزودن اشتراک' if active is None else 'ویرایش اشتراک'
    middle_label = ttk.Label(subscribe_frame, text=title, font=("Helvetica", 16))
    middle_label.grid(row=0, column=1, padx=10, pady=5)

    # Name
    name_label = ttk.Label(subscribe_frame, text=person[2]+" "+person[3], font=("Helvetica", 16))
    name_label.grid(row=1, column=0, padx=10, pady=5)

    # Start Date
    tk.Label(subscribe_frame, text="تاریخ شروع").grid(row=2, column=1, padx=10, pady=5)
    entry_start_date = tk.Entry(subscribe_frame)
    entry_start_date.insert(0, start_date)
    entry_start_date.grid(row=2, column=0, padx=10, pady=5)

    # End Date
    tk.Label(subscribe_frame, text="تاریخ پایان").grid(row=3, column=1, padx=10, pady=5)
    entry_end_date = tk.Entry(subscribe_frame)
    entry_end_date.insert(0, end_date)
    entry_end_date.grid(row=3, column=0, padx=10, pady=5)

    # Num of Sessions
    tk.Label(subscribe_frame, text="کل جلسات").grid(row=4, column=1, padx=10, pady=5)
    entry_num_sessions = tk.Entry(subscribe_frame)
    entry_num_sessions.insert(0, num_of_sessions)
    entry_num_sessions.grid(row=4, column=0, padx=10, pady=5)

    # Num of Remaining Sessions
    tk.Label(subscribe_frame, text="جلسات باقیمانده").grid(row=5, column=1, padx=10, pady=5)
    entry_remaining_sessions = tk.Entry(subscribe_frame)
    entry_remaining_sessions.insert(0, remaining_sessions)
    entry_remaining_sessions.grid(row=5, column=0, padx=10, pady=5)

    # Delete Button
    if active is not None:
        delete_button = tk.Button(subscribe_frame, text="حذف", command=delete_subscription, bg="red", fg="white", height=2)
        delete_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Apply Button
        apply_button = tk.Button(subscribe_frame, text="ویرایش اشتراک", command=update_subscription, bg=color, fg="white", height=2)
        apply_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
    
    else:
        # Apply Button
        apply_button = tk.Button(subscribe_frame, text="افزودن اشتراک", command=save_subscription, bg=color, fg="black", height=2)
        apply_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

    # Cancel Button
    cancel_button = tk.Button(subscribe_frame, text="لغو", command=cancel_subscription, bg="red", fg="white", height=2)
    cancel_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
