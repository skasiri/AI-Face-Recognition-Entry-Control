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

    return known_frame