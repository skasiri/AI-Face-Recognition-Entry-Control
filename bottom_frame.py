import os
import tkinter as tk
from tkinter import ttk
import cv2
import pickle



def create_bottom_frame(parent):
    bottom_frame = ttk.Frame(parent, padding="10", relief="solid")
    bottom_label = ttk.Label(bottom_frame, text="Operations", font=("Helvetica", 16))
    bottom_label.pack(pady=10)

    return bottom_frame