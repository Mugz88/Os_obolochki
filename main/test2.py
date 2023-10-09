import tkinter as tk
import psutil
import os
from datetime import datetime
from tkinter import filedialog

def show_process_info():
    current_pid = os.getpid()
    current_processes = []
    child_processes = []

    for process in psutil.process_iter(attrs=['pid', 'name', 'ppid']):
        if process.info['ppid'] == current_pid:
            child_processes.append(process)
        elif process.info['pid'] == current_pid:
            current_processes.append(process)
    
    # Retrieve child processes using the psutil.Process().children() method
    for process in current_processes:
        child_processes.extend(process.children())
    
    info = ""
    
    for process in current_processes:
        info += f"PID: {process.info['pid']}, Creation Date: {datetime.fromtimestamp(process.create_time())}\n"
    
    for process in child_processes:
        info += f"Child PID: {process.info['pid']}, Creation Date: {datetime.fromtimestamp(process.create_time())}\n"
    
    window = tk.Tk()
    window.title("Process Information")
    
    text = tk.Text(window)
    text.insert(tk.END, info)
    text.pack()
    
    def save_to_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(info)
    
    save_button = tk.Button(window, text="Save to File", command=save_to_file)
    save_button.pack()
    
    window.mainloop()

show_process_info()