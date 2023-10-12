import tkinter as tk
import psutil
import os
from datetime import datetime
from tkinter import filedialog
import time
import multiprocessing


def update_process_info(window, text):
    current_pid = os.getpid()
    current_processes = []
    child_processes = []

    for process in psutil.process_iter(['pid', 'name', 'ppid', 'create_time']):
        if process.ppid() == current_pid:
            child_processes.append(process)
        elif process.pid == current_pid:
            current_processes.append(process)
    
    parent_process = psutil.Process(current_pid).parent()
    if parent_process is not None:
        current_processes.append(parent_process)
    
    info = ""
    
    for process in current_processes:
        info += f"PID: {process.pid}, Name: {process.name()}, Creation Date: {datetime.fromtimestamp(process.create_time())}\n"
    
    for process in child_processes:
        info += f"Child PID: {process.pid}, Name: {process.name()}, Creation Date: {datetime.fromtimestamp(process.create_time())}\n"
    
    text.insert(tk.END, info)
    print(current_pid)
    window.after(10000, update_process_info, window, text) 

def show_process_info():
    window = tk.Tk()
    window.title("Process Information")
    
    text = tk.Text(window)
    text.pack()
    
    def save_to_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(text.get(1.0, tk.END))
    
    save_button = tk.Button(window, text="Save to File", command=lambda: save_to_file())
    save_button.pack()
    test_button = tk.Button(window, text="Test", command=create_processes_with_tkinter)
    test_button.pack(anchor="ne")
    update_process_info(window, text) 
    
    window.mainloop()

def create_processes_with_tkinter():
    def test():
        print("Creating a new process...")
        time.sleep(2)
        print("Process created!")

    def create_process():
        test_process = multiprocessing.Process(target=test)
        test_process.start()

    def start_creating_processes():
        create_process()
        window.after(5000, start_creating_processes)

    window = tk.Tk()
    window.title("Process Creator")

    start_button = tk.Button(window, text="Start Creating Processes", command=start_creating_processes)
    start_button.pack()
    
    window.mainloop()



