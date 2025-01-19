import os
import tkinter as tk
from tkinter import ttk
import cv2
import pickle
from liveview_frame import camera_option, ip_camera_connection_string, set_camera, start_stream, on_air, grayscale, set_grayscale


def create_bottom_frame(parent):
    
    camera = tk.StringVar(value=camera_option)
    connection_string = tk.StringVar(value=ip_camera_connection_string)
    grayscale_process = tk.BooleanVar(value=grayscale)

    def show_config_window():

        def save_config():
            set_camera(camera.get())
            set_grayscale(grayscale_process.get())
            if not on_air:
                set_camera(camera.get())
                start_stream()

            with open("config.pkl", "wb") as f:
                data = (camera.get(), connection_string.get(), grayscale_process.get())
                pickle.dump(data, f)

            print("Configuration saved")
            config_window.destroy()


        # Create a new window
        config_window = tk.Toplevel(bottom_frame)
        config_window.title("Configuration")
        config_window.geometry("640x480")

        # Create a frame for camera selection
        camera_frame = ttk.Frame(config_window)
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
        ip_camera_entry = ttk.Entry(camera_frame, textvariable=connection_string)

        # Function to toggle visibility
        def toggle_ip_camera_entry(*args):
            if camera.get() == "ip":
                ip_camera_label.grid(row=1, column=1, sticky="nsew")
                ip_camera_entry.grid(row=1, column=2, columnspan=2, sticky="nsew")
            else:
                ip_camera_label.grid_remove()
                ip_camera_entry.grid_remove()

        # Trace the camera variable to call the toggle function
        camera.trace_add("write", toggle_ip_camera_entry)

        # Call toggle function initially to set the correct visibility
        toggle_ip_camera_entry()

        
        # Create a frame for BW process switch
        bw_frame = ttk.Frame(config_window)
        bw_frame.pack(fill="both", expand=True)


        # Create a switch for Grayscale process
        bw_switch = ttk.Checkbutton(bw_frame, text="Grayscale", variable=grayscale_process, onvalue=True, offvalue=False)
        bw_switch.pack(side="left", padx=10)

        # Create a button to save the configuration
        save_button = ttk.Button(config_window, text="Save", command=save_config)
        save_button.pack(pady=10)


    def show_config_window1():
        
        def save_config():
            set_camera(camera.get())
            if not on_air:
                set_camera(camera.get())
                start_stream()

            with open("config.pkl", "wb") as f:
                pickle.dump((camera.get(), connection_string.get()), f)

            print("Configuration saved")
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

        # Create a frame for BW process switch
        bw_frame = ttk.Frame(config_frame)
        bw_frame.pack(fill="both", expand=True)

        # Create a label for BW process
        bw_label = ttk.Label(bw_frame, text="BW Process:")
        bw_label.pack(side="left", padx=10)

        # Create a switch for BW process
        bw_switch = ttk.Checkbutton(bw_frame, text="Enable")
        bw_switch.pack(side="right", padx=10)


        # Create a button to save the configuration
        save_button = ttk.Button(config_frame, text="Save", command=save_config)
        save_button.pack(pady=10)


    bottom_frame = ttk.Frame(parent, padding="10", relief="solid")

    bottom_label = ttk.Label(bottom_frame, text="Operations", font=("Helvetica", 16))
    bottom_label.pack(pady=10)

    config_button = ttk.Button(bottom_frame, text="Configuration", command=show_config_window)
    config_button.pack(pady=10)

    return bottom_frame
