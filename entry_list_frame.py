import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


tree = None

def create_entry_list_frame(parent):
    global tree

    entry_frame = ttk.Frame(parent, padding="10", relief="solid")
    entry_frame.grid(row=0, column=0, sticky="nsew")

    # Create a treeview to display the table
    tree = ttk.Treeview(entry_frame, columns=("row", "melli", "mobile", "timeSpent", "lastSeen", "enterAt", "name"), show="headings")
    tree.heading("row", text="Row", anchor=tk.E)
    tree.heading("melli", text="National Code", anchor=tk.E)
    tree.heading("name", text="Name", anchor=tk.E)
    tree.heading("mobile", text="Mobile", anchor=tk.E)
    tree.heading("enterAt", text="Entrance", anchor=tk.E)
    tree.heading("lastSeen", text="Last Detect", anchor=tk.E)
    tree.heading("timeSpent", text="Time Spent", anchor=tk.E)

    # Configure column widths to fit content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col), anchor=tk.E)

    # Create a scrollbar to scroll horizontally
    xscrollbar = ttk.Scrollbar(entry_frame, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    tree.config(xscrollcommand=xscrollbar.set)
    xscrollbar.config(command=tree.xview)

    # Create a scrollbar to scroll vertically
    yscrollbar = ttk.Scrollbar(entry_frame, orient=tk.VERTICAL)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=tree.yview)

    # Bind the event to the treeview
    tree.pack(fill="both", expand=True)

    return entry_frame
