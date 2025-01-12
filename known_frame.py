import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from utils.encodings import remove_face_from_list
from liveview_frame import create_edit_dialog, create_subscribe_form
from utils.face_list import get_known_faces_list
from utils.subscription import Subscription

known_update_frame = True
def create_known_frame(parent):

    known_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    known_label = ttk.Label(known_frame, text="Known", font=("Helvetica", 16))
    known_label.pack(fill="x")

    # Create a canvas and scrollbar
    canvas = tk.Canvas(known_frame, width=120)

    # Add a switch for live view
    live_view_var = tk.BooleanVar(value=True)  # Variable to hold the state of the switch

    def toggle_live_view():
        global known_update_frame
        if live_view_var.get():
            # Code to turn on live view
            known_update_frame = True
            print("Live view turned on")
            # Resume the update_images_thread or start live view processing

        else:
            # Code to turn off live view
            known_update_frame = False
            print("Live view turned off")
            # Pause or stop the update_images_thread or halt live view processing

    # Create the switch button
    live_view_switch = ttk.Checkbutton(
        known_frame, text="Live View", variable=live_view_var, command=toggle_live_view
    )
    live_view_switch.pack(pady=5)

    canvas_frame = ttk.Frame(known_frame)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, width=120)

    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

    known_scrollable_frame = ttk.Frame(canvas)

    known_scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=known_scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    
    image_size = (85, 85)

    def display_images(image_list):
        for item in image_list:
            melli, name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
            image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(known_scrollable_frame, image=photo)
            image_label.image = photo
            image_label.pack(pady=5)

            sub = Subscription()
            active = sub.get_active_subscription(melli)
            color = "green" if active is not None else "yellow"

            name_label = ttk.Label(known_scrollable_frame, text=name, font=("Tahoma", 12), background=color)
            name_label.pack(pady=(0, 5))
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(known_scrollable_frame)
            button_frame.pack(pady=5)

            # Load icons for the buttons
            edit_icon = ImageTk.PhotoImage(Image.open("icons/person-edit.png").resize((20, 20)))
            subscribe_active_icon = ImageTk.PhotoImage(Image.open("icons/timer-edit.png").resize((20, 20)))
            subscribe_inactive_icon = ImageTk.PhotoImage(Image.open("icons/timer-alert.png").resize((20, 20)))

            subscribe_icon = subscribe_active_icon if active is not None else subscribe_inactive_icon

            # Create the remove button
            edit_button = ttk.Button(button_frame, image=edit_icon, command=lambda melli=melli: edit_person(melli, image_list))
            edit_button.image = edit_icon
            edit_button.pack(side="left", padx=5)
            # Create the register button
            subscribe_button = ttk.Button(button_frame, image=subscribe_icon, command=lambda melli=melli: subscribe(melli))
            subscribe_button.image = subscribe_icon
            subscribe_button.pack(side="left", padx=5)

            image_label.config(borderwidth=2, relief="solid", background=color)


    def edit_person(melli, image_list):
        print(f"Edit person: {melli}")
        create_edit_dialog(melli, image_list)

    def subscribe(melli):
        print(f"Subscribe person: {melli}")
        create_subscribe_form(melli)

    def update_images():
        global known_update_frame
        while True:
            if known_update_frame is False:
                time.sleep(3)
                continue

            known_faces_list = get_known_faces_list()
            for widget in known_scrollable_frame.winfo_children():
                widget.destroy()
            display_images(known_faces_list)
            time.sleep(3)

    # Initial display of images
    update_images_thread = threading.Thread(target=update_images)
    update_images_thread.daemon = True  # Set as daemon thread so it stops when the main thread exits

    # Start the thread
    update_images_thread.start()

    return known_frame