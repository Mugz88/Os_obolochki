import getpass
import tkinter as tk
import socket
from datetime import datetime, timedelta
import os
import time
import threading

def doubleWin():
    class Main(tk.Frame):
        def __init__(self):
            def on_file_new():
                print("New file")

            def on_file_open():
                print("Open file")

            def on_file_save():
                print("Save file")
            global test
            test = False
            self.root = tk.Toplevel()
            self.root.geometry('800x600')
            self.root.resizable(width = False, height = False)
            self.root.title("Second Window")
            # Создание меню
            self.menu_bar = tk.Menu(self.root)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            #menu_bar.add_cascade(label="File", menu=file_menu)
            self.menu_bar.add_command(label="Мусор")
            self.menu_bar.add_cascade(label="Tools")
            self.menu_bar.add_command(label="Второе окно")
            self.menu_bar.add_command(label="Терминал")
            self.menu_bar.add_command(label="Процессы")
            self.menu_bar.add_command(label="Логи")	
            self.menu_bar.add_command(label="Поиск")
            self.menu_bar.add_command(label="Справка")

            #top frame
            self.title_frame = tk.Frame(self.root)
            self.title_frame.pack(fill = 'both', expand = True)
            self.info_button = tk.Button(self.title_frame, text = "?", width = 1, height = 1)
            self.info_button.pack(side = 'right',anchor="nw")
            #back button
            self.back_button = tk.Button(self.title_frame, text = "..", width = 1, height = 1)
            self.back_button.pack(side = 'left',anchor="nw")

            #path entry
            self.pat_text = tk.StringVar()
            self.pat_text.set("path")
            self.current_path = tk.Entry(self.title_frame, textvariable = self.pat_text, width = 80, state='readonly')
            self.current_path.pack(side = 'left',anchor="nw",fill="x")

            #button show/hidde hidden dir/file
            self.hiden_dir = tk.IntVar()
            self.check_button = tk.Checkbutton(self.title_frame, text = "Hidden", font = ("Helvetica", 10), padx = 1, pady = 1, variable = self.hiden_dir)
            self.check_button.pack(side = 'left',anchor="nw")

            # Установка меню в окне
            self.root.config(menu=self.menu_bar)
            #main frame
            self.main_frame = tk.Frame(self.root)
            self.main_frame.pack()
            def update_clock():
                '''функция обновления времени'''
                new = datetime.now()
                self.time_label.configure(text=new.strftime("%H:%M:%S"))
                self.root.after(1000, update_clock)
            #time running
            self.time_label = tk.Label(self.main_frame, text=" ")
            self.time_label.pack(side = 'right', anchor='se')
            update_clock()


            #USB devices
            self.usbFrame = tk.Frame(self.main_frame)
            self.usbFrame.pack(side = 'left', anchor='n')
            self.update_device_list()
        
       
            # scroll bar
            self.scrollbar_vert = tk.Scrollbar(self.main_frame, orient="vertical")
            self.scrollbar_vert.pack(side = 'right', fill = 'y')

            self.scrollbar_hor = tk.Scrollbar(self.main_frame, orient="horizontal")
            self.scrollbar_hor.pack(side = 'bottom', fill = 'x')

            #canvas
            self.canvas = tk.Canvas(self.main_frame, borderwidth=0,  bg = 'white')
            self.inner_frame = tk.Frame(self.canvas,  bg = 'white')

            #команды для прокрутки
            self.scrollbar_vert["command"] = self.canvas.yview
            self.scrollbar_hor["command"] = self.canvas.xview

            #настройки для canvas
            self.canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand = self.scrollbar_hor.set, width=600, heigh=550)

            self.canvas.pack(side='left', fill='both', expand=True)
            self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
            SuperName = "Baza"
            SuperPath = os.path.abspath("")+"/"+SuperName+"/"
            path=SuperPath+"buff.txt"
            def update_buff():
                def client_function():
                    HOST = '127.0.0.1'
                    PORT = 12445

                    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_sock.connect((HOST, PORT))

                    print(f'Установлено соединение с {HOST}:{PORT}')

                    while True:
                        data = client_sock.recv(1024)
                        if not data:
                            break
                        data = data.decode("utf-8")
                        print(f'Получено сообщение от сервера: {data}', end='\r')

                        for widget in self.inner_frame.winfo_children():
                            widget.destroy()
                        lines = []
                        i = 0
                        #with open(path, 'r') as file:
                        #    lines = file.readlines()
                        lines = data.split('\n')
                        self.pat_text.set(lines[0])
                        for item in lines[1].split(" "):
                            folder_name = tk.Label(self.inner_frame, text=item,  bg = 'white')
                            folder_name.grid(row=i, sticky='w')
                            i+=1
                        if (lines[2]=="t r u e"):
                            self.hiden_dir.set(1)
                        else:
                            self.hiden_dir.set(0)
                        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                        self.canvas.yview_moveto(0)
                        

                        #time.sleep(0.01)

                    client_sock.close()
                client_thread = threading.Thread(target=client_function)
                client_thread.start()
                global test
                if test:
                    client_thread.join()
                #self.root.after(1000, update_buff)
                
            update_buff()
            
              
            #отрисовываем содержимое лиректории
        def get_media_devices(self):
            username = getpass.getuser()
            media_path = os.path.join('/media', username)

            if not os.path.exists(media_path):
                return []

            devices = os.listdir(media_path)
            return devices
        def update_device_list(self):
            devices = self.get_media_devices()

            self.usbFrame.update_idletasks()  # Обновить виджеты перед обновлением списка

            # Удалить все виджеты
            for widget in self.usbFrame.winfo_children():
                widget.pack_forget()

            if devices:
                for device in devices:
                    button = tk.Button(self.usbFrame, text=device, cursor="hand2")
                    button.pack()

            self.root.after(1000, self.update_device_list)
    def on_closing():
        # Завершаем потоки.
        global test
        test = True
        
        # Закрываем окно.
        win.root.destroy()
        # установить окно поверх других окон
    win = Main()
    win.root.attributes('-topmost', 1)
    # поднять окно поверх других окон
    win.root.lift()
    win.root.protocol('WM_DELETE_WINDOW', on_closing)
    win.root.mainloop()
