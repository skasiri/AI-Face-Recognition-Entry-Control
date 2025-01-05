import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

known_update_frame = True
def create_known_frame(parent):

    known_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    known_label = ttk.Label(known_frame, text="Known", font=("Helvetica", 16))
    known_label.pack(fill="x")

    return known_frame