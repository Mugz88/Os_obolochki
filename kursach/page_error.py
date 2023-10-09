import os
import tkinter as tk
import subprocess
def display_page_errors():
    PID = os.getpid()
    command = "ps -o min_flt,maj_flt "+str(PID)
    try:
        page_errors = subprocess.check_output(command, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        page_errors = "Error retrieving page errors"
    
    root = tk.Tk()
    root.title("Page Errors")
    root.geometry('200x50')
    
    label = tk.Label(root, text="{}".format(page_errors))
    label.pack()
    
    root.mainloop()

# Example usage:
