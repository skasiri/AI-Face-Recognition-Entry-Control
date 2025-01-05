import os
import tkinter as tk
from tkinter import ttk
import cv2
import pickle



def create_bottom_frame(parent):
    bottom_frame = ttk.Frame(parent, padding="10", relief="solid")

    bottom_label = ttk.Label(bottom_frame, text="Operations", font=("Helvetica", 16))
    bottom_label.pack(pady=10)

    config_button = ttk.Button(bottom_frame, text="Configuration", command=show_config_window)
    config_button.pack(pady=10)



    return bottom_frame

def show_config_window():
    pass