import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bottom_frame import create_bottom_frame
from entry_list_frame import create_entry_list_frame
from unknown_frame import create_unknown_frame
from known_frame import create_known_frame

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

# Create entry list frame
entry_frame = create_entry_list_frame(main_frame)
entry_frame.grid(row=0, column=0, sticky="nsew")

# Create known faces frame
known_frame = create_known_frame(main_frame)
known_frame.grid(row=0, column=2, sticky="nsew")

# Create unknown faces frame
unknown_frame = create_unknown_frame(main_frame)
unknown_frame.grid(row=0, column=3, sticky="nsew")


# Create bottom row
bottom_frame = create_bottom_frame(main_frame)
bottom_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")





def on_app_exit():
    # release_freshest_frame()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_app_exit)

root.mainloop()