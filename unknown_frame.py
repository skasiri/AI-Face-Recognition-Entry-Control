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
def create_unknown_frame(parent):

    unknown_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    unknown_label = ttk.Label(unknown_frame, text="Unknown", font=("Helvetica", 16))
    unknown_label.pack(fill="x")

    # Create a canvas and scrollbar
    canvas = tk.Canvas(unknown_frame, width=120)

    # Add a switch for live view
    live_view_var = tk.BooleanVar(value=True)  # Variable to hold the state of the switch

    def toggle_live_view():
        global unknown_update_frame
        if live_view_var.get():
            # Code to turn on live view
            unknown_update_frame = True
            print("Live view turned on")
            # Resume the update_images_thread or start live view processing

        else:
            # Code to turn off live view
            unknown_update_frame = False
            print("Live view turned off")
            # Pause or stop the update_images_thread or halt live view processing

    # Create the switch button
    live_view_switch = ttk.Checkbutton(
        unknown_frame, text="Live View", variable=live_view_var, command=toggle_live_view
    )
    live_view_switch.pack(pady=5)

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
            image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(scrollable_frame, image=photo)
            image_label.image = photo
            image_label.pack(pady=(0, 5))

            name_label = ttk.Label(scrollable_frame, text=name, font=("Helvetica", 12))
            name_label.pack(pady=5)
            
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(scrollable_frame)
            button_frame.pack(pady=5)
            # Load icons for the buttons
            remove_icon = ImageTk.PhotoImage(Image.open("icons/eye-remove.png").resize((20, 20)))
            register_icon = ImageTk.PhotoImage(Image.open("icons/account-plus.png").resize((20, 20)))
            # Create the remove button
            remove_button = ttk.Button(button_frame, image=remove_icon, command=lambda name=name: remove_image(name))
            remove_button.image = remove_icon
            remove_button.pack(side="left", padx=5)
            # Create the register button
            register_button = ttk.Button(button_frame, image=register_icon, command=lambda name=name: register_image(name, image_list))
            register_button.image = register_icon
            register_button.pack(side="left", padx=5)

    def remove_image(name):
        remove_face_from_list(name)

    def register_image(name, image_list):
        create_register_dialog(name, image_list)

    def update_images():
        global unknown_update_frame
        while True:
            if unknown_update_frame is False:
                time.sleep(3)
                continue
            unknown_faces_list = get_unknown_faces_list()
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            display_images(unknown_faces_list)
            time.sleep(3)
    
    # Initial display of images
    update_images_thread = threading.Thread(target=update_images)
    update_images_thread.daemon = True  # Set as daemon thread so it stops when the main thread exits

    # Start the thread
    update_images_thread.start()
    
    return unknown_frame