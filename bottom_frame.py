import os
import tkinter as tk
from tkinter import ttk
import cv2
import pickle
from liveview_frame import camera_option, ip_camera_connection_string, set_camera


def create_bottom_frame(parent):
    
    camera = tk.StringVar(value=camera_option)
    connection_string = tk.StringVar(value=ip_camera_connection_string)

    def show_config_window():
        
        def save_config():
            with open("config.pkl", "wb") as f:
                pickle.dump((camera.get(), connection_string.get()), f)
            print("Configuration saved")
            set_camera(camera.get())
            config_window.destroy()
            
        # Create a new window
        config_window = tk.Toplevel(bottom_frame)
        config_window.title("Configuration")
        config_window.geometry("640x480")
        # Create a frame to hold the widgets
        config_frame = ttk.Frame(config_window)
        config_frame.pack(fill="both", expand=True)
        # Create frame to choose camera
        camera_frame = ttk.Frame(config_frame)
        camera_frame.pack(fill="both", expand=True)
        # Create radio buttons for camera options
        camera_frame.columnconfigure(0, weight=0)
        camera_frame.columnconfigure(1, weight=0)
        camera_frame.columnconfigure(2, weight=1)
        
        local_camera_rb = ttk.Radiobutton(camera_frame, text="Local Camera", variable=camera, value="local")
        local_camera_rb.grid(row=0, column=1, sticky="nsew")

        ip_camera_rb = ttk.Radiobutton(camera_frame, text="IP Camera", variable=camera, value="ip")
        ip_camera_rb.grid(row=0, column=2, sticky="nsew")

        # Create entry for IP camera connection string
        ip_camera_label = ttk.Label(camera_frame, text="IP Camera Connection String:")
        ip_camera_label.grid(row=1, column=1, sticky="nsew")
        ip_camera_entry = ttk.Entry(camera_frame, textvariable=connection_string)
        ip_camera_entry.grid(row=1, column=2, columnspan=2, sticky="nsew")

        # Create a button to save the configuration
        save_button = ttk.Button(config_frame, text="Save", command=save_config)
        save_button.pack(pady=10)


    bottom_frame = ttk.Frame(parent, padding="10", relief="solid")

    bottom_label = ttk.Label(bottom_frame, text="Operations", font=("Helvetica", 16))
    bottom_label.pack(pady=10)

    config_button = ttk.Button(bottom_frame, text="Configuration", command=show_config_window)
    config_button.pack(pady=10)

    return bottom_frame
