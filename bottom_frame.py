import os
import tkinter as tk
from tkinter import ttk
import cv2
import pickle
from liveview_frame import camera_option, ip_camera_connection_string, set_camera, start_stream, on_air, grayscale, set_grayscale, frame_size_ratio, set_frame_size_ratio, stop_stream

def create_bottom_frame(parent):
    
    camera = tk.StringVar(value=camera_option)
    connection_string = tk.StringVar(value=ip_camera_connection_string)
    grayscale_process = tk.BooleanVar(value=grayscale)
    size_ratio = 100 // int(frame_size_ratio * 100)
    resize_value = tk.IntVar(value=size_ratio)

    def show_config_window():

        def save_config():

            stop_stream()
            
            frame_size_ratio_new = (100 / resize_value.get()) / 100
            set_frame_size_ratio(frame_size_ratio_new)

            set_grayscale(grayscale_process.get())
            
            if camera.get() != camera_option:
                set_camera(camera.get())


            if not on_air:
                stop_stream()
                set_camera(camera.get())
                start_stream()

            with open("config.pkl", "wb") as f:
                data = (camera.get(), connection_string.get(), grayscale_process.get(), frame_size_ratio_new)
                pickle.dump(data, f)

            print("Configuration saved")
            config_window.destroy()


        # Create a new window
        config_window = tk.Toplevel(bottom_frame)
        config_window.title("Configuration")
        config_window.geometry("640x480")

        # Create a frame for camera selection
        camera_frame = ttk.Frame(config_window)
        camera_frame.pack(fill="both", padx=10, pady=10)

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
                ip_camera_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
                ip_camera_entry.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=10, pady=10)
            else:
                ip_camera_label.grid_remove()
                ip_camera_entry.grid_remove()

        # Trace the camera variable to call the toggle function
        camera.trace_add("write", toggle_ip_camera_entry)

        # Call toggle function initially to set the correct visibility
        toggle_ip_camera_entry()

        
        # Create a frame for BW process switch
        bw_frame = ttk.Frame(config_window)
        bw_frame.pack(fill="both", pady=10)


        # Create a switch for Grayscale process
        bw_switch = ttk.Checkbutton(bw_frame, text="Grayscale", variable=grayscale_process, onvalue=True, offvalue=False)
        bw_switch.pack(side="left", padx=10)

        # Create a frame for resize value selection
        resize_frame = ttk.Frame(config_window)
        resize_frame.pack(fill="both", padx=10, pady=10)

        # Create a label for resize value selection
        resize_label = ttk.Label(resize_frame, text="Resize ratio:")
        resize_label.pack(side="left")

        # Create a slider for resize value selection
        resize_options = [0, 1, 2, 4, 8]
        # resize_variable = tk.IntVar(value=resize_options[0])
        resize_option_menu = ttk.OptionMenu(resize_frame, resize_value, *resize_options)
        resize_option_menu.pack(side="left")

        # Create a button to save the configuration
        save_button = ttk.Button(config_window, text="Save", command=save_config)
        save_button.pack(padx=10, pady=10, side="bottom")


    bottom_frame = ttk.Frame(parent, padding="10", relief="solid")

    bottom_label = ttk.Label(bottom_frame, text="Operations", font=("Helvetica", 16))
    bottom_label.pack(pady=10)

    config_button = ttk.Button(bottom_frame, text="Configuration", command=show_config_window)
    config_button.pack(pady=10)

    return bottom_frame
