import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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