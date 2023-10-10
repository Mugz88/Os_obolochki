import tkinter as tk

def create_info_window():
    # Создание нового окна
    window = tk.Tk()

    # Создание фрейма
    frame = tk.Frame(window)
    frame.pack()

    # Информация о программе
    info_text = "Программа для отображения информации"
    info_label = tk.Label(frame, text=info_text)
    info_label.pack()

    # Функция для закрытия окна
    def close_window():
        window.destroy()

    # Кнопка для закрытия окна
    button = tk.Button(frame, text="ОК", command=close_window)
    button.pack()

    # Запуск главного цикла окна
    window.mainloop()
