import tkinter as tk
from multiprocessing import Process, Queue

def new_process(queue):
    # Создание окна Tkinter
    window = tk.Toplevel()
    window.title("Real-time Data Copy")

    # Создание метки для отображения данных
    label = tk.Label(window, text="")
    label.pack()

    # Получение данных из очереди и обновление метки в реальном времени
    def update_label():
        while True:
            if not queue.empty():
                data = queue.get()
                # Обновление метки с полученными данными
                label.config(text=data)
                window.update_idletasks()

    # Запуск функции обновления метки в отдельном потоке
    process = Process(target=update_label)
    process.start()

def new_window():
    # Создание очереди для обмена данными
    queue = Queue()

    # Функция для отправки данных во второе окно
    def send_data():
        data = entry.get()
        queue.put(data)

    # Создание главного окна Tkinter
    main_window = tk.Tk()
    main_window.title("Main Window")

    # Создание поле ввода данных
    entry = tk.Entry(main_window)
    entry.pack()

    # Создание кнопки для вызова функции и отправки данных
    button = tk.Button(main_window, text="Create Second Window", command=lambda: new_process(queue))
    button.pack()

    # Создание кнопки для отправки данных
    send_button = tk.Button(main_window, text="Send Data", command=send_data)
    send_button.pack()

    main_window.mainloop()

    # Дождитесь завершения процесса
    process.join()

