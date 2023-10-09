import os
import tkinter as tk
import psutil
filename = "2 lab/file.txt"
page_size = os.sysconf("SC_PAGE_SIZE")
file_size = os.path.getsize(filename)
working_set_size = (file_size // page_size) * page_size
root = tk.Tk()
mem_info_label = tk.Label(root, text="")
mem_info_label.pack()

def update_mem_info():
    # получаем информацию о памяти с помощью psutil
    mem_info = psutil.Process(os.getpid()).memory_info()

    # выводим информацию в метку
    mem_info_label.configure(text="Working set size: {} bytes".format(mem_info.rss))

root.title("rabotaet")
mem_info_label = tk.Label(root, text="")

mem_info_label.pack()
update_button = tk.Button(root, text=" Buffer Info", command=update_mem_info)
update_button.pack()


lable = tk.Label(root, text="pid")
lable.pack()
inp = tk.Entry(root)
inp.pack()
lable1 = tk.Label(root, text="address")
lable1.pack()
inp1 = tk.Entry(root)
inp1.pack()
lable2 = tk.Label(root, text="val")
lable2.pack()
inp2 = tk.Entry(root)
inp2.pack()

res = tk.Entry(root)
res.pack()

def write():
    pid = int(inp.get())
    maps_file = open(f"/proc/{pid}/mem", 'rb+')
    maps_file.seek(int(inp1.get(), 0))
    maps_file.write(bytes.fromhex(inp2.get()))
    maps_file.close()

def read():
    pid = int(inp.get())
    print(pid)
    maps_file = open(f"/proc/{pid}/mem", 'rb+')
    maps_file.seek(int(inp1.get(), 0))
    data = maps_file.read(1)
    res.delete(0, len(res.get()))
    res.insert(0,data.__str__())
    maps_file.close()


but1 = tk.Button(root, text="read", command=read)
but1.pack()
but2 = tk.Button(root, text="write", command=write)
but2.pack()

root.mainloop()
