import tkinter as tk
from tkinter import ttk


tree = None

def create_entry_list_frame(parent):
    global tree

    entry_frame = ttk.Frame(parent, padding="10", relief="solid")
    entry_frame.grid(row=0, column=0, sticky="nsew")

    return entry_frame
