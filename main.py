import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bottom_frame import create_bottom_frame

camera_source = 0
ip_camera_connection_string = ""

root = tk.Tk()
root.title("AI face recognition entry system By Saeidksr")
root.geometry("1024x768")

# Create main frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Configure grid layout
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=0)  # Smaller column
main_frame.columnconfigure(3, weight=0)  # Smaller column
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=0)  # Smaller row


# Create bottom row
bottom_frame = create_bottom_frame(main_frame)




def on_app_exit():
    # release_freshest_frame()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_app_exit)

root.mainloop()