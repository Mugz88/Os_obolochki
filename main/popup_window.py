import tkinter as tk
import threading

class PopupWindow(tk.Toplevel):
    def __init__(self, sock):
        super().__init__()

        self.title("Popup Window")
        self.geometry("300x200")

        self.label = tk.Label(self, text="Waiting for data...")
        self.label.pack(pady=20)

        self.sock = sock

        threading.Thread(target=self.receive_data).start()

    def send_data(self, data):
        self.sock.sendall(data.encode())

    def receive_data(self):
        while True:
            data = self.sock.recv(1024).decode()
            self.label.config(text=data)

if __name__ == "__main__":
    window = tk.Tk()
    window.withdraw()
    popup = PopupWindow()
    window.mainloop()
