import os
from random import randint
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from utils.encodings import remove_face_from_list, unknown_faces_list, known_face_names, known_face_melli
from liveview_frame import create_edit_dialog, create_subscribe_form
from utils.face_list import get_known_faces_list, known_faces_list
from utils.subscription import Subscription

known_update_frame = True
# known_faces_list = []
image_frames = []

def create_known_frame(parent):

    known_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    known_label = ttk.Label(known_frame, text="Known", font=("Helvetica", 16))
    known_label.pack(fill="x")

    # Create a canvas and scrollbar
    canvas = tk.Canvas(known_frame, width=120)

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

    def create_image_frame(melli, name, face_image):
            
            box = ttk.Frame(known_scrollable_frame)
            if not image_frames:
                box.pack(pady=5)
            else:
                box.pack(before=image_frames[0][0], pady=5)

            image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image)

            image_frame = ttk.Label(box, image=photo)
            image_frame.image = photo
            image_frame.pack(pady=5)

            sub = Subscription()
            active = sub.get_active_subscription(melli)
            color = "green" if active is not None else "yellow"

            name_label = ttk.Label(box, text=name, font=("Tahoma", 12), background=color)
            name_label.pack(pady=(0, 5))
            # Create a frame to hold the buttons
            button_frame = ttk.Frame(box)
            button_frame.pack(pady=5)

            # Load icons for the buttons
            edit_icon = ImageTk.PhotoImage(Image.open("icons/person-edit.png").resize((20, 20)))
            subscribe_active_icon = ImageTk.PhotoImage(Image.open("icons/timer-edit.png").resize((20, 20)))
            subscribe_inactive_icon = ImageTk.PhotoImage(Image.open("icons/timer-alert.png").resize((20, 20)))
            subscribe_icon = subscribe_active_icon if active is not None else subscribe_inactive_icon
            person_cry_icon = ImageTk.PhotoImage(Image.open("icons/person-cry.png").resize((20, 20)))

            # Create the wrong detect button
            cry_button = ttk.Button(button_frame, image=person_cry_icon, command=lambda melli=melli: remove_image_frame(melli))
            cry_button.image = person_cry_icon
            cry_button.pack(side="left", padx=5)

            # Create the remove button
            edit_button = ttk.Button(button_frame, image=edit_icon, command=lambda melli=melli: create_edit_dialog(melli))
            edit_button.image = edit_icon
            edit_button.pack(side="left", padx=5)

            # Create the register button
            subscribe_button = ttk.Button(button_frame, image=subscribe_icon, command=lambda melli=melli: create_subscribe_form(melli))
            subscribe_button.image = subscribe_icon
            subscribe_button.pack(side="left", padx=5)


            image_frame.config(borderwidth=2, relief="solid", background=color)

            return box

    def update_image_frame(melli, name, face_image):
        for box, image_melli in image_frames:
            if image_melli == melli:

                image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, image_size, interpolation=cv2.INTER_LANCZOS4)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image)

                box_image = box.winfo_children()[0]
                box_image.config(image=photo)
                box_image.image = photo

    def remove_image_frame(melli):
        # def handle_remove(melli):
            dialog = tk.Toplevel()
            dialog.title("Remove Confirmation")

            frame = ttk.Frame(dialog)
            frame.pack(padx=10, pady=10)

            label = ttk.Label(frame, text="Are you sure this face is wrong detected?")
            label.pack(pady=5)

            button_frame = ttk.Frame(frame)
            button_frame.pack(pady=5)

            def add_to_unknown():
                global unknown_faces_list, known_faces_list
                
                for box, image_melli in image_frames:
                    if image_melli == melli:
                        name = f"Unknown{randint(0, 1000)}"
                        for item in known_faces_list:
                            if item[0] == melli:  # Assuming melli is the unique identifier
                                image = item[2]
                                face_encoding = item[5]  # Assuming the face_encoding is at index 5
                                unknown_faces_list.append((name, image, None, [], face_encoding, int(time.time()), int(time.time())))
                                known_face_names.remove(item[1])
                                known_face_melli.remove(item[0])
                                known_faces_list.remove(item)
                                box.destroy()
                                image_frames.remove((box, image_melli))
                                break
                        break
                        
                dialog.destroy()

            def another_person():
                # create_edit_dialog(melli)
                dialog.destroy()

            def cancel():
                dialog.destroy()

            unknown_button = ttk.Button(button_frame, text="Add to Unknown", command=add_to_unknown)
            unknown_button.pack(side="left", padx=5)

            another_button = ttk.Button(button_frame, text="Another Person", command=another_person)
            another_button.pack(side="left", padx=5)

            cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel)
            cancel_button.pack(side="left", padx=5)



    def update_images():
        global known_update_frame, known_faces_list
        while True:
            if known_update_frame is False:
                time.sleep(3)
                continue

            known_faces_list = get_known_faces_list()

            for item in known_faces_list:
                melli, name, face_image, confidence, landmarks_list, face_encoding, insertAt, updateAt = item  # Assuming the tuple contains (name, face_image, confidence)
                if not any(image_melli == melli for _, image_melli in image_frames):
                    image_frame = create_image_frame(melli, name, face_image)
                    image_frames.insert(0, (image_frame, melli))
                else:
                    update_image_frame(melli, name, face_image)

            time.sleep(1)

    # Initial display of images
    update_images_thread = threading.Thread(target=update_images)
    update_images_thread.daemon = True  # Set as daemon thread so it stops when the main thread exits

    # Start the thread
    update_images_thread.start()

    return known_frame