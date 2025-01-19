import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from utils.encodings import remove_face_from_list
from liveview_frame import create_register_dialog
from utils.face_list import get_unknown_faces_list

unknown_update_frame = True
image_frames = []

def create_unknown_frame(parent):

    unknown_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    unknown_label = ttk.Label(unknown_frame, text="Unknown", font=("Helvetica", 16))
    unknown_label.pack(fill="x")

    # Create a canvas and scrollbar
    canvas = tk.Canvas(unknown_frame, width=120)

    canvas_frame = ttk.Frame(unknown_frame)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, width=120)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    image_size = (85, 85)

    
    def display_images(image_list):
        for item in image_list:
            name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
            box = create_image_frame(name, face_image)
            image_frames.append((box, name))

    def create_image_frame(item):
            name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
                        
            box = ttk.Frame(scrollable_frame)
            if not image_frames:
                box.pack(pady=5)
            else:
                box.pack(before=image_frames[0][0], pady=5)

            image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(box, image=photo)
            image_label.image = photo
            image_label.pack(pady=(0, 5))

            name_label = ttk.Label(box, text=name, font=("Helvetica", 12))
            name_label.pack(pady=5)
            
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(box)
            button_frame.pack(pady=5)
            # Load icons for the buttons
            remove_icon = ImageTk.PhotoImage(Image.open("icons/eye-remove.png").resize((20, 20)))
            register_icon = ImageTk.PhotoImage(Image.open("icons/account-plus.png").resize((20, 20)))
            # Create the remove button
            remove_button = ttk.Button(button_frame, image=remove_icon, command=lambda name=name: remove_image(name))
            remove_button.image = remove_icon
            remove_button.pack(side="left", padx=5)
            # Create the register button
            register_button = ttk.Button(button_frame, image=register_icon, command=lambda name=name: create_register_dialog(item))
            register_button.image = register_icon
            register_button.pack(side="left", padx=5)

            return box

    def update_image_frame(name, face_image):
        for box, image_name in image_frames:
            if image_name == name:

                image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image)

                box_image = box.winfo_children()[0]
                box_image.config(image=photo)
                box_image.image = photo

    def remove_image(name):
        for box, image_name in image_frames:
            if image_name == name:
                remove_face_from_list(name)
                box.destroy()
                image_frames.remove((box, name))
                break

    def register_image(name, image_list):
        create_register_dialog(name, image_list)

    def update_images():
        global unknown_update_frame
        while True:
            if unknown_update_frame is False:
                time.sleep(1)
                continue

            unknown_faces_list = get_unknown_faces_list()
            
            for item in unknown_faces_list:
                name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
                if not any(image_name == name for _, image_name in image_frames):
                    image_frame = create_image_frame(item)
                    image_frames.insert(0, (image_frame, name))
                else:
                    update_image_frame(name, face_image)

            time.sleep(1)
    
    # Initial display of images
    update_images_thread = threading.Thread(target=update_images)
    update_images_thread.daemon = True  # Set as daemon thread so it stops when the main thread exits

    # Start the thread
    update_images_thread.start()
    
    return unknown_frame