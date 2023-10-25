import tkinter
import os
import subprocess
import shutil
import time
import threading
import getpass

from datetime import datetime, timedelta
from tkinter import messagebox
from tkinter import simpledialog, Label, Tk
from tkinter.messagebox import OK, INFO
from page_error import display_page_errors
from mycloak import cloaks
from wifi_info import display_wifi_info
from terminal import myterm
from finder import finder
#from doublewindow import new_window
from process import show_process_info
from info import create_info_window


SuperName = "Baza"
SuperPath = os.path.abspath("")+"/"+SuperName+"/"
os.mkdir(SuperPath)
os.mkdir(SuperPath+"System")
os.mkdir(SuperPath+"MyDoc")
os.mkdir(SuperPath+"ProgramFile")
os.mkdir(SuperPath+"System"+"/"+"Trash")
os.mkdir(SuperPath+"System"+"/"+"Logs")
os.mkdir(SuperPath+"System"+"/"+"Utilities")
os.system("sudo chattr +i "+SuperPath+"System/")


class TrashContexMenu(tkinter.Menu):
    '''Контекстное меню для корзины'''
    def __init__(self, main_window, parent):
        super(TrashContexMenu, self).__init__(parent, tearoff = 0)
        self.main_window = main_window
        #self.add_command(label="Очистить козину", command = self.clear_trash) это переместить !!!
        self.add_command(lavel="Восстановить", command=self.recover)
        
    def clear_trash(self):
        '''функция для очистки корзины'''
        full_path = self.main_window.path_text.get() + self.main_window.selected_file
        if os.path.isdir(full_path):
            #выполняем команду отдельным процессом
            process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            #при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Проблема при удалении", 'У Вас нет прав для удаления')
        self.main_window.refresh_window()
    def recover(self):
        '''Функиця восстановления данных из корзины'''
      ####################################переделать  
    def popup_menu(self, event):
        ''' функция для активации контекстного меню'''
        self.post(event.x_root, event.y_root)
        #если активны другие меню - отменяем их
        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()
        if self.main_window.file_context_menu:
            self.main_window.file_context_menu.unpost()
        self.main_window.selected_file = event.widget["text"]
			
class MainContextMenu(tkinter.Menu):
	''' Контекстное меню для внутренней области директории'''
	def __init__(self, main_window, parent):
		super(MainContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Создать директорию", command = self.create_dir)
		self.add_command(label="Создать файл", command = self.create_file)
		

	def popup_menu(self, event):
		''' функция для активации контекстного меню'''
		#если активны другие меню - отменяем их
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		if self.main_window.dir_context_menu:
			self.main_window.dir_context_menu.unpost()
		self.post(event.x_root, event.y_root)

	def create_dir(self):
		''' функция для создания новой директории в текущей'''
		dir_name = simpledialog.askstring("Новая директория", "Введите название новой директории")
		if dir_name:
			command = "mkdir {0}".format(dir_name).split(' ')
			#выполняем команду отдельным процессом
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!","Отказано в доступе.")
			self.main_window.refresh_window()
		log_action("Создана новая директория "+dir_name)

	def create_file(self):
		''' функция для создания нового файла в текущей директории'''
		dir_name = simpledialog.askstring("Новый файл", "Введите название нового файла")
		if dir_name:
			command = "touch {0}".format(dir_name).split(' ')
			#выполняем команду отдельным процессом
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!","Отказано в доступе.")
			self.main_window.refresh_window()
		log_action("Создан новый файл "+dir_name)


	def insert_to_dir(self):
		''' функция для копирования файла или директории в текущую директорию'''
		copy_obj = self.main_window.buff
		to_dir = self.main_window.path_text.get()
		if os.path.isdir(self.main_window.buff):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Операция невозможна!", err.decode("utf-8"))
		else:
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!",err.decode("utf-8"))
		self.main_window.refresh_window()
		log_action("Объект: "+copy_obj+" был скопирован в "+to_dir)
  
		
	def drop(self):
		'''функция переноса'''
		for i in range(len(self.main_window.drag_and_drop)):
			buffi = [i for i in self.main_window.drag_and_drop[i].split('/') if i]
			j = i
			while j < len(self.main_window.drag_and_drop):
				
				buffj = [i for i in self.main_window.drag_and_drop[j].split('/') if i]
				for word in buffj[:-1]:    
					if buffi[-1] == word:
						bl = self.main_window.drag_and_drop[i]
						self.main_window.drag_and_drop[i] = self.main_window.drag_and_drop[j]
						self.main_window.drag_and_drop[j] = bl
				j+=1
		for obj in self.main_window.drag_and_drop:
			copy_obj = obj
			to_dir = self.main_window.path_text.get()
			if os.path.isdir(obj):
				#выполняем команду отдельным процессом
				process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				out, err = process.communicate()
				if err:
					messagebox.showwarning("Операция невозможна!", err.decode("utf-8"))
			else:
				#выполняем команду отдельным процессом
				process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				out, err = process.communicate()
				#при возникновении ошибки выводим сообщение
				if err:
					messagebox.showwarning("Операция невозможна!",err.decode("utf-8"))
			full_path = obj
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['rm','-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при удалении файла", 'У Вас нет прав для удаления данного файла')
			log_action("Объект: "+copy_obj+" был перенесен в "+to_dir)
		self.main_window.refresh_window()
		self.main_window.clear_drag()
	
class FileContextMenu(tkinter.Menu):
	def __init__(self, main_window, parent):
		super(FileContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Открыть файл", command = self.open_file)
		self.add_separator()
		self.add_command(label="Копировать", command = self.copy_file)
		self.add_command(label="Переименовать", command = self.rename_file)
		self.add_command(label="Drag", command=self.drag_file )
		self.add_separator()
		self.add_command(label="Удалить в корзину", command = self.delete_file)
		self.add_command(label="Удалить", command=self.del_file)


	def open_file(self):
		''' функция для открытия файла сторонними программами'''
		ext = self.main_window.take_extention_file(self.main_window.selected_file)
		full_path = self.main_window.path_text.get() + self.main_window.selected_file

		if ext in ['txt', 'py', 'html', 'css', 'js']:
			if 'mousepad' in self.main_window.all_program:
				subprocess.Popen(["mousepad", full_path], start_new_session = True)
			else:
				self.problem_message()
		elif ext == 'pdf':
			if 'evince' in self.main_window.all_program:
				subprocess.run(["evince", full_path], start_new_session = True)
			else:
				self.problem_message()
		elif ext in ['png', 'jpeg', 'jpg', 'gif']:
			if 'ristretto' in self.main_window.all_program:
				subprocess.run(["ristretto", full_path], start_new_session = True)
			else:
				self.problem_message()
		else:
			self.problem_message()

	def problem_message(self):
		messagebox.showwarning("Проблема при открытии файла", 'Прости, но я не могу открыть этот файл')

	def drag_file(self):
		self.main_window.drag_and_drop.append(self.main_window.path_text.get() + self.main_window.selected_file)
		print(self.main_window.drag_and_drop)
		self.main_window.refresh_window()
 
	def copy_file(self):
		''' функция для копирования файла'''
		#заносим полный путь к файлу в буффер
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		self.main_window.refresh_window()


	def delete_file(self):
		''' функция для удаления выбранного файла'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		copy_obj = self.main_window.buff
		to_dir = SuperPath+"System"+"/"+"Trash/"
		if os.path.isdir(self.main_window.buff):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			
		else:
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
		
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		#выполняем команду отдельным процессом
		process = subprocess.Popen(['rm', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, err = process.communicate()
		#при возникновении ошибки выводим сообщение
		if err:
			messagebox.showwarning("Проблема при удалении файла", 'У Вас нет прав для удаления данного файла')
		self.main_window.refresh_window()
		log_action("Файл: "+self.main_window.selected_file+" был перемещен в корзину")
  
	def del_file(self):
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		#выполняем команду отдельным процессом
		process = subprocess.Popen(['rm', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, err = process.communicate()
		#при возникновении ошибки выводим сообщение
		if err:
			messagebox.showwarning("Проблема при удалении файла", 'У Вас нет прав для удаления данного файла')
		self.main_window.refresh_window()
		log_action("Файл: "+self.main_window.selected_file+" был удален")
  
	def rename_file(self):
		''' функция для переименования выбранного файла'''
		new_name = simpledialog.askstring("Переименование файла", "Введите новое название файла")
		if new_name:
			old_file = self.main_window.path_text.get() + self.main_window.selected_file
			new_file = self.main_window.path_text.get() + new_name
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при переименовании файла", 'У Вас нет прав для переименования данного файла')
			self.main_window.refresh_window()
		log_action("файл: "+self.main_window.selected_file+" был переименован в "+new_name)

	def popup_menu(self, event):
		''' функция для активации контекстного меню'''
		self.post(event.x_root, event.y_root)
		#если активны другие меню - отменяем их
		if self.main_window.main_context_menu:
			self.main_window.main_context_menu.unpost()
		if self.main_window.dir_context_menu:
			self.main_window.dir_context_menu.unpost()
		self.main_window.selected_file = event.widget["text"]

class DirContextMenu(tkinter.Menu):
	def __init__(self, main_window, parent):
		super(DirContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Переименовать", command = self.rename_dir)
		self.add_command(label="Копировать", command = self.copy_dir)
		self.add_command(label="Drag", command=self.drag_dir)
		self.add_separator()
		self.add_command(label="Удалить в корзину", command = self.delete_dir)
		self.add_command(label="Удалить", command=self.del_dir)
	
	def drag_dir(self):
		'''функция для взятия директории'''
		self.main_window.drag_and_drop.append(self.main_window.path_text.get() + self.main_window.selected_file)
		print(self.main_window.drag_and_drop)
		self.main_window.refresh_window()
 
	def copy_dir(self):
		''' функция для копирования директории'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		self.main_window.refresh_window()

	def delete_dir(self):
		''' функция для удаления выбранной директории'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		copy_obj = self.main_window.buff
		to_dir = SuperPath+"System"+"/"+"Trash/"
		if os.path.isdir(self.main_window.buff):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			
		else:
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			
		
  
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		if os.path.isdir(full_path):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при удалении директории", 'У Вас нет прав для удаления данной директории')
		self.main_window.refresh_window()
		log_action("Директория: "+self.main_window.selected_file+" была перемещена в корзину")
  
	def del_dir(self):
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		if os.path.isdir(full_path):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при удалении директории", 'У Вас нет прав для удаления данной директории')
		self.main_window.refresh_window()
		log_action("Директория: "+self.main_window.selected_file+" была навсегда утрачена")
  
	def rename_dir(self):
		''' функция для переименования выбранной директории'''
		new_name = simpledialog.askstring("Переименование директории", "Введите новое название директории")
		if new_name:
			old_dir = self.main_window.path_text.get() + self.main_window.selected_file
			new_dir = self.main_window.path_text.get() + new_name
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['mv', old_dir, new_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при переименовании директории", 'У Вас нет прав для переименования данной директории')
			self.main_window.refresh_window()
		log_action("Директория: "+self.main_window.selected_file+" была переименнована в "+new_name)
	def popup_menu(self, event):
		''' функция для активации контекстного меню'''
		self.post(event.x_root, event.y_root)
		#если активны другие меню - отменяем их
		if self.main_window.main_context_menu:
			self.main_window.main_context_menu.unpost()
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		self.main_window.selected_file = event.widget["text"]

class MainWindow(tkinter.Frame):
	''' Класс основного окна'''
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title("SuperApp")
		self.root.resizable(width = False, height = False)
		self.root.geometry('800x600')	
		self.hidden_dir = tkinter.IntVar()
		self.buff = None
		self.drag_and_drop = []
		self.all_program = os.listdir("/home/sany/snap/")
		log_action("Программа запущена")

		self.root.bind('<Button-1>', self.root_click)
		self.root.bind('<FocusOut>', self.root_click)

		#menubar
		menu = tkinter.Menu(self.root)
		tools = tkinter.Menu(menu, tearoff=0)
		tools.add_command(label="page errors", command=display_page_errors)
		tools.add_command(label="Wifi info", command=display_wifi_info)
		tools.add_command(label="Cloak", command=cloaks)
		
		
		menu.add_command(label="Мусор", command=self.to_trash)
		menu.add_cascade(label="Tools", menu=tools)
		menu.add_command(label="Второе окно", command="")
		menu.add_command(label="Терминал", command=myterm)
		menu.add_command(label="Процессы", command=show_process_info)
		menu.add_command(label="Логи", command=open_log_window)	
		menu.add_command(label="Поиск", command=finder)
		menu.add_command(label="Справка", command=create_info_window)
		#menu.add_command()
		self.root.config(menu=menu)

		#top frame
		self.title_frame = tkinter.Frame(self.root)
		self.title_frame.pack(fill = 'both', expand = True)
		self.info_button = tkinter.Button(self.title_frame, text = "?", command = self.info_program, width = 1, height = 1)
		self.info_button.pack(side = 'right',anchor="nw")

		#trashBoxButton
		#self.into_button = tkinter.Button(self.title_frame, text="мусор", command=self.to_trash, width=2,height=2)
		#self.into_button.pack(side = 'bottom', anchor = "w")
  
	
		#back button
		self.back_button = tkinter.Button(self.title_frame, text = "..", command = self.parent_dir, width = 1, height = 1)
		self.back_button.pack(side = 'left',anchor="nw")
		self.back_button.bind("<b>", lambda event: button_click(event))
  
		#path entry
		self.path_text = tkinter.StringVar()
		self.path_text.set(SuperPath)
		self.current_path = tkinter.Entry(self.title_frame, textvariable = self.path_text, width = 80, state='readonly')
		self.current_path.pack(side = 'left',anchor="nw",fill="x")

		#button show/hidde hidden dir/file
		self.check_button = tkinter.Checkbutton(self.title_frame, text = "Hidden", font = ("Helvetica", 10), padx = 1, pady = 1, variable = self.hidden_dir, command = self.refresh_window)
		self.check_button.pack(side = 'left',anchor="nw")

		#main frame
		self.main_frame = tkinter.Frame(self.root)
		self.main_frame.pack()
  
		#time running
		self.time_label = tkinter.Label(self.main_frame, text=" ")
		self.time_label.pack(side = 'right', anchor='se')
		self.update_clock()

		#USB devices
		self.usbFrame = tkinter.Frame(self.main_frame)
		self.usbFrame.pack(side = 'left', anchor='n')
		self.update_device_list()
  
		# scroll bar
		self.scrollbar_vert = tkinter.Scrollbar(self.main_frame, orient="vertical")
		self.scrollbar_vert.pack(side = 'right', fill = 'y')

		self.scrollbar_hor = tkinter.Scrollbar(self.main_frame, orient="horizontal")
		self.scrollbar_hor.pack(side = 'bottom', fill = 'x')

		#canvas
		self.canvas = tkinter.Canvas(self.main_frame, borderwidth=0,  bg = 'white')
		self.inner_frame = tkinter.Frame(self.canvas,  bg = 'white')

		#команды для прокрутки
		self.scrollbar_vert["command"] = self.canvas.yview
		self.scrollbar_hor["command"] = self.canvas.xview

		#настройки для canvas
		self.canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand = self.scrollbar_hor.set, width=600, heigh=550)

		self.canvas.pack(side='left', fill='both', expand=True)
		self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

		#отрисовываем содержимое лиректории
		self.dir_content()

		#binds
		self.root.bind("<b>", lambda event:self.parent_dir())
		self.root.bind("<Control-w>", lambda event:on_closing())
		self.root.bind("<F1>", lambda event:create_info_window())
		self.root.bind("<t>", lambda event:self.to_trash())
		self.root.bind("<Control-s>", lambda event:finder())

	def root_click(self, event):
		''' функция для обработки события клика в root'''
		#если есть контекстные меню - отменяем
		
		if self.file_context_menu:
			self.file_context_menu.unpost()
		if self.main_context_menu:
			self.main_context_menu.unpost()
		if self.dir_context_menu:
			self.dir_context_menu.unpost()

	def dir_content(self):
		''' функция для определения содержимого текущей директории'''
		#содержимое в текущей директории
		dir_list = os.listdir(self.path_text.get())
		path = self.path_text.get()
		
  
		if not dir_list:
			#общее контекстное меню
			self.main_context_menu = MainContextMenu(self, self.canvas)
			self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
			if self.buff:
				self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_dir)
			if self.drag_and_drop:
				self.main_context_menu.add_command(label="Drop",command=self.main_context_menu.drop )
				self.main_context_menu.add_command(label="Clear Drag", command=self.clear_drag)
			self.inner_frame.bind('<Button-3>', self.main_context_menu.popup_menu)
			#контекстное меню для файлов
			self.file_context_menu = None
			#контекстное меню для директории
			self.dir_context_menu = None
			return None

		#общее контекстное меню
		self.main_context_menu = MainContextMenu(self, self.canvas)
		self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
		if self.buff:
			self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_dir)
		if self.drag_and_drop:
			self.main_context_menu.add_command(label="Drop",command=self.main_context_menu.drop )
			self.main_context_menu.add_command(label="Clear Drag", command=self.clear_drag)
		#контекстное меню для файлов
		self.file_context_menu = FileContextMenu(self, self.inner_frame)
		#контекстное меню для директории
		self.dir_context_menu = DirContextMenu(self, self.inner_frame)


		i = 0
		for item in dir_list:

			if os.path.isdir(str(path) + item):
				#обрабатываем директории
				if os.access(str(path) + item, os.R_OK):
					if (not self.hidden_dir.get() and  not item.startswith('.')) or self.hidden_dir.get():
						
						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white', cursor = 'hand1')
						folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.bind("<Button-3>", self.dir_context_menu.popup_menu)
						folder_name.grid(row=i+1, column=1, sticky='w')
				else:
					if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
						
						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
						folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.grid(row=i+1, column=1, sticky='w')

			else:
				#обрабатываем файлы
				if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
					ext = self.take_extention_file(item)
					#фото, картинки
					if ext in ['jpeg', 'jpg', 'png', 'gif']:
						file_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
						file_name.grid(row=i+1, column=1, sticky='w')

						file_name.bind("<Button-3>", self.file_context_menu.popup_menu)
					else:
						#другие файлы
						if os.access(str(path) + item, os.R_OK):
							
							folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
							folder_name.grid(row=i+1, column=1, sticky='w')

							folder_name.bind("<Button-3>", self.file_context_menu.popup_menu)

						else:
							folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
							folder_name.grid(row=i+1, column=1, sticky='w')
			i += 1
		#обновляем inner_frame и устанавливаем прокрутку для нового содержимого
		self.inner_frame.update()
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
  
	def clear_drag(self):
		self.drag_and_drop = []
		self.refresh_window()

	def move_to_dir(self, event):
		''' функция для перехода в выбранную директорию'''
		elem = event.widget
		dir_name = elem["text"]
		fool_path = self.path_text.get() + dir_name
		if os.path.isdir(fool_path) and os.access(fool_path, os.R_OK):
			old_path = self.path_text.get()
			self.path_text.set(old_path + dir_name + '/')
			self.root_click('<Button-1>')
			self.refresh_window()
   
	def to_trash(self):
		''' функция перехода в корзину'''
		old_path = [i for i in self.path_text.get().split('/') if i]
		new_path = '/'+'/'.join(old_path[:-1])
		if not new_path:
			new_path = SuperPath+"System"+"/"+"Trash/"
		if os.path.isdir(new_path):
			if new_path == SuperPath+"System"+"/"+"Trash/":
				self.path_text.set(new_path)
    
			else:
				self.path_text.set(SuperPath+"System"+"/"+"Trash/")
			self.refresh_window()
  
	def info_program(self):
		messagebox.showinfo(title="О программе",message="Операционные системы и оболочки, Python", 
            detail="Натальин А.Ю, ИВТ-13", icon=INFO, default=OK)
                      
    
	def parent_dir(self):
		''' функция для перемещения в родительскую директорию'''
		old_path = [i for i in self.path_text.get().split('/') if i]
		new_path = '/'+'/'.join(old_path[:-1])
		if not new_path:
			new_path = SuperPath
		if os.path.isdir(new_path):
			if new_path == SuperPath:
				self.path_text.set(new_path)
    
			else:
				self.path_text.set(SuperPath)
			self.refresh_window()


	def take_extention_file(self, file_name):
		''' функция для получения расширения файла'''
		ls = file_name.split('.')
		if len(ls)>1:
			return ls[-1]
		else:
			return None

	def refresh_window(self):
		''' функция для обновления текущего отображения директорий/файлов'''
		for widget in self.inner_frame.winfo_children():
				widget.destroy()
		self.dir_content()
		self.canvas.yview_moveto(0)
  
	def trash_cheak(self):
		'''Функция проверки находится ли пользователь в корзине'''
		var = self.path_text.get().split('/')
		for i in var:
			if i == "Trash":
				return True
		return False	
	

	time_work = 0
	def update_clock(self):
		'''функция обновления времени'''
		now = timedelta(seconds=self.time_work)
		self.time_label.configure(text=now)
		self.time_work+=1
		self.root.after(1000, self.update_clock)
  
	def get_media_devices(self):
		username = getpass.getuser()
		media_path = os.path.join('/media', username)

		if not os.path.exists(media_path):
			return []

		devices = os.listdir(media_path)
		return devices

	def show_device_path(self, device_path):
		self.path_text.set(device_path+"/")
		print("Device path:", device_path)
		self.refresh_window()

	def handle_button_click( self, device):
		device_path = os.path.join('/media', getpass.getuser(), device)
		self.show_device_path(device_path)

	def update_device_list(self):
		devices = self.get_media_devices()

		self.usbFrame.update_idletasks()  # Обновить виджеты перед обновлением списка

		# Удалить все виджеты
		for widget in self.usbFrame.winfo_children():
			widget.pack_forget()

		if devices:
			for device in devices:
				button = tkinter.Button(self.usbFrame, text=device, cursor="hand2", command=lambda d=device: self.handle_button_click(d))
				button.pack()

		self.root.after(1000, self.update_device_list)
log_message = ""

def log_action(action):
    global log_message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message += f"{timestamp} - {action}\n"

def open_log_window():
    def save_logs_to_file():
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs_{timestamp}.txt"
        logpath = SuperPath+"/System/Logs/"+filename
        with open(logpath, "w") as file:
            file.write(log_message)
            

    def show_logs():
        def on_closing():
            nonlocal stop_emulation
            stop_emulation = True
            save_logs_to_file()
            log_window.destroy()

        def update_logs():
            log_text.delete("1.0", tkinter.END)
            log_text.insert(tkinter.END, log_message)
            log_text.update()
            if not stop_emulation:
                log_text.after(100, update_logs)

        stop_emulation = False

        log_window = tkinter.Tk()
        log_window.title("Логи")

        log_text = tkinter.Text(log_window, width=50, height=20)
        log_text.pack()

        save_button = tkinter.Button(log_window, text="Сохранить", command=save_logs_to_file)
        save_button.pack()

        log_window.protocol("WM_DELETE_WINDOW", on_closing)

        threading.Thread(target=update_logs, daemon=True).start()

        log_window.mainloop()
    show_logs()

def button_click(event):
    button_name = event.widget.cget("text")
    log_action(f"{button_name} была использована")
def on_closing():
    os.system("sudo chattr -R -i "+SuperPath)
    shutil.rmtree(SuperPath)
    win.root.destroy()  # Закрыть окно

print(os.getpid())
win = MainWindow()
win.root.protocol("WM_DELETE_WINDOW", on_closing)
win.root.mainloop()

