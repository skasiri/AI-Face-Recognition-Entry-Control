import os
import threading
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

unknown_update_frame = True
def create_unknown_frame(parent):

    unknown_frame = ttk.Frame(parent, padding="10", relief="solid")
    
    unknown_label = ttk.Label(unknown_frame, text="Unknown", font=("Helvetica", 16))
    unknown_label.pack(fill="x")

    return unknown_frame