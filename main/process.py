import os
import psutil
import tkinter as tk
from tkinter import ttk

def get_processes():
    current_pid = os.getpid()
    processes = []
    print(current_pid)
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
        if proc.info['pid'] != current_pid:
            pid = proc.info['pid']
            name = proc.info['name']
            status = proc.info['status']
            cpu_percent = proc.info['cpu_percent']
            memory_percent = proc.info['memory_percent']
            processes.append(f"PID: {pid} | Name: {name} | Status: {status} | CPU %: {cpu_percent} | Memory %: {memory_percent}")

    return processes

def update_processes(process_listbox):
    process_listbox.delete(0, tk.END)

    processes = get_processes()

    process_listbox.insert(tk.END, "PID\tName\tStatus\tCPU %\tMemory %")
    process_listbox.insert(tk.END, "-" * 50)

    for process in processes:
        process_listbox.insert(tk.END, process)

    process_listbox.after(15000, lambda: update_processes(process_listbox))

def process_view():
    root = tk.Tk()
    root.title("Process Viewer")
    root.geometry("800x400")

    process_frame = ttk.Frame(root)
    process_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    process_listbox = tk.Listbox(process_frame)
    process_listbox.pack(fill=tk.BOTH, expand=True)

    update_processes(process_listbox)

    root.mainloop()
