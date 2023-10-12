import tkinter as tk

def create_info_window():
    # Создание нового окна
    window = tk.Tk()
    window.title("Справка")
    # Создание фрейма
    frame = tk.Frame(window)
    frame.pack()

    # Наполнение окна информацией
    info_text = "Программа для отображения горячих клавиш"
    info_label = tk.Label(frame, text=info_text)
    info_label.pack()
    label = tk.Label(frame, text="Ctrl+W - закрытие программы")
    label.pack()
    label = tk.Label(frame, text="Ctrl+S - открыть поиск")
    label.pack()
    label = tk.Label(frame, text="T - перейти в корзину")
    label.pack()
    label = tk.Label(frame, text="F1 - открыть справку")
    label.pack()
    label = tk.Label(frame, text="B - перейти в домашнюю директорию")
    label.pack()
    # Функция для закрытия окна
    def close_window():
        window.destroy()

    # Кнопка для закрытия окна
    button = tk.Button(frame, text="ОК", command=close_window)
    button.pack()

    # Запуск главного цикла окна
    window.mainloop()
