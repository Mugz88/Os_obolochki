import tkinter as tk
import threading
import socket
import time
def send_message():
    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Подключаемся к серверу
    server_address = ('localhost', 12325)

    while True:
        try:
            client_socket.connect(server_address)
            break
        except ConnectionRefusedError:
            print("Server is not available, trying to connect...")
            time.sleep(1)  # Пауза в 1 секунду
            continue

    try:
        # Отправляем данные серверу
        message = 'Hello, server!'
        client_socket.sendall(message.encode())

        # Получаем данные от сервера
        amount_received_data = client_socket.recv(1024)
        received_data = amount_received_data.decode()

        print('Received data: ', received_data)  # Выводим полученные данные

    finally:
        # Закрываем соединение
        client_socket.close()

# Создаем главное окно
root = tk.Tk()

# Создаем кнопку "Send" и добавляем ее в окно
send_button = tk.Button(root, text="Send", command=lambda: threading.Thread(target=send_message).start())
send_button.pack()

# Запускаем главный цикл приложения
root.mainloop()
