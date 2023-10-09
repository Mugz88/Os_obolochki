from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button

def send_message():
    message = input_field.get("1.0", END).strip()
    input_field.delete("1.0", END)
    display_message("You: " + message)
    # Обработка сообщения и формирование ответа
    response = process_message(message)
    display_message("Bot: " + response)

def display_message(message):
    chat_history.configure(state="normal")
    chat_history.insert(END, message + "\n")
    chat_history.configure(state="disabled")
    chat_history.see(END)

def process_message(message):
    # Предположим, что здесь будет ваш код для обработки сообщения и формирования ответа
    # В данном примере просто возвращаем обратно сообщение пользователя
    return message

def create_chat_window():
    root = Tk()
    root.title("Chat")

    # Создаем главный фрейм
    main_frame = Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Создаем поле для истории чата
    chat_history = Text(main_frame, wrap="word", state="disabled")
    chat_history.pack(side="left", fill="both", expand=True)

    # Добавляем скроллбар для поля истории чата
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=chat_history.yview)
    scrollbar.pack(side="right", fill="y")

    # Привязываем скроллбар к полю истории чата
    chat_history["yscrollcommand"] = scrollbar.set

    # Создаем фрейм для поля ввода и кнопки отправки сообщения
    input_frame = Frame(root)
    input_frame.pack(side="bottom", fill="x")

    # Создаем поле для ввода сообщения
    input_field = Text(input_frame, wrap="word")
    input_field.pack(side="left", fill="both", expand=True)

    # Создаем кнопку отправки сообщения
    send_button = Button(input_frame, text="Send", command=send_message)
    send_button.pack(side="right")

    # Назначаем фокус на поле ввода
    input_field.focus()

    # Запускаем главный цикл обработки событий
    root.mainloop()

create_chat_window()

