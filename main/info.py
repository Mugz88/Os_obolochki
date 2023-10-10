import tkinter as tk

def create_info_window():
    # Создание нового окна
    window = tk.Tk()

    # Добавление текстового поля
    text = tk.Text(window)
    text.pack()

    # Функция для закрытия окна
    def close_window():
        window.destroy()

    # Кнопка для закрытия окна
    button = tk.Button(window, text="ОК", command=close_window)
    button.pack()

    # Запуск главного цикла окна
    window.mainloop()
