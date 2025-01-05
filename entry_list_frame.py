import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


tree = None

def create_entry_list_frame(parent):
    global tree

    entry_frame = ttk.Frame(parent, padding="10", relief="solid")
    entry_frame.grid(row=0, column=0, sticky="nsew")

    # Create a treeview to display the table
    tree = ttk.Treeview(entry_frame, columns=( "melli", "mobile", "timeSpent", "lastSeen", "enterAt", "name", "row"), show="headings")
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


# Add a function to add a new item to the table
def add_attendance_row(melli, name, mobile, enter_at, last_seen, time_spent):
    global tree
    enter_at = enter_at.strftime("%H:%M")
    last_seen = last_seen.strftime("%H:%M")
    time_spent = str(time_spent).split(' ')[2]
    row = len(tree.get_children())
    tree.insert("", 0, values=(melli, mobile, time_spent, last_seen, enter_at, name, row))
    
# Add a function to remove an item from the table by melli
def remove_item(melli):
    global tree
    if melli:
        for item in tree.get_children():
            if tree.set(item, "melli") == melli:
                tree.delete(item)
                break

def clear_attendance_rows():
    global tree
    for item in tree.get_children():
        tree.delete(item)