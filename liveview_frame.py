import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from jdatetime import datetime as jdt

parent_frame = None
middle_frame = None

def create_live_view_frame(parent):
    global parent_frame, middle_frame
    parent_frame = parent
    middle_frame = ttk.Frame(parent, padding="10", relief="solid")
    middle_label = ttk.Label(middle_frame, text="Live View", font=("Helvetica", 16))
    middle_label.pack(pady=10)
    
    return middle_frame