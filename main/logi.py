import tkinter as tk
import threading
from datetime import datetime

def open_log_window():
    log_message = ""

    def log_action(action):
        nonlocal log_message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message += f"{timestamp} - {action}\n"

    def save_logs_to_file():
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs_{timestamp}.txt"
        with open(filename, "w") as file:
            file.write(log_message)

    def show_logs():
        def on_closing():
            nonlocal stop_emulation
            stop_emulation = True
            save_logs_to_file()
            log_window.destroy()

        def update_logs():
            log_text.delete("1.0", tk.END)
            log_text.insert(tk.END, log_message)
            log_text.update()
            if not stop_emulation:
                log_text.after(100, update_logs)

        stop_emulation = False

        log_window = tk.Tk()
        log_window.title("Логи")

        log_text = tk.Text(log_window, width=50, height=20)
        log_text.pack()

        save_button = tk.Button(log_window, text="Сохранить", command=save_logs_to_file)
        save_button.pack()

        log_window.protocol("WM_DELETE_WINDOW", on_closing)

        threading.Thread(target=update_logs, daemon=True).start()

        log_window.mainloop()

    log_action("Программа запущена")
    show_logs()