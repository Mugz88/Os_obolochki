import tkinter as tk
from tkinter import filedialog
import os
def finder():
    def search_path():
        query = search_entry.get()
        results = []
        
        if query:
            for root_dir, dirs, files in os.walk("."):
                for name in dirs + files:
                    if query.lower() in name.lower():
                        results.append(os.path.join(root_dir, name))
        
        results_list.delete(0, tk.END)
        
        if results:
            for result in results:
                results_list.insert(tk.END, result)
        else:
            results_list.insert(tk.END, "Нет результатов")

    root = tk.Tk()
    root.title("Поисковик")

    search_label = tk.Label(root, text="Введите название файла или директории:")
    search_label.pack()

    search_entry = tk.Entry(root, width=50)
    search_entry.pack()

    search_button = tk.Button(root, text="Поиск", command=search_path)
    search_button.pack()

    results_list = tk.Listbox(root, width=100)
    results_list.pack()

    root.mainloop()