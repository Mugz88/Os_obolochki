import os
import getpass
import tkinter as tk

def get_media_devices():
    username = getpass.getuser()
    media_path = os.path.join('/media', username)

    if not os.path.exists(media_path):
        return []

    devices = os.listdir(media_path)
    return devices

def show_device_path(device_path):
    print("Device path:", device_path)

def handle_button_click(device):
    device_path = os.path.join('/media', getpass.getuser(), device)
    show_device_path(device_path)

def update_device_list():
    devices = get_media_devices()

    device_frame.update_idletasks()  # Обновить виджеты перед обновлением списка

    # Удалить все виджеты
    for widget in device_frame.winfo_children():
        widget.pack_forget()

    if devices:
        for device in devices:
            button = tk.Button(device_frame, text=device, cursor="hand2", command=lambda d=device: handle_button_click(d))
            button.pack()

    root.after(1000, update_device_list)

def main():
    global device_frame, root

    root = tk.Tk()
    root.title("Media Devices")

    device_frame = tk.Frame(root)
    device_frame.pack()

    update_device_list()

    root.mainloop()

if __name__ == '__main__':
    main()