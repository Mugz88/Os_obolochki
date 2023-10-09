from threading import Condition, Lock
import threading
def check_mutex():
    global mutex_a, mutex_b
    mutex_a.lock()
    mutex_b.lock()
#Проверка взаимной блокировки и выход из нее
    mutex_a = Lock()
    mutex_b = Lock()    
    condition = Condition()
    task_a = threading.Thread(target=task_a)
    task_b = threading.Thread(target=task_b)

    task_a.start()
    task_b.start()
check_mutex()
while True:
    condition.wait(mutex_a) #Ждем освобождения ресурса X от task_a
#Получаем доступ к ресурсу Y от task_b
#Выполняем работу с ресурсом Y
    condition.notify() #Освобождаем ресурс Y для task_b
    condition.wait_for(mutex_b) #Ждем освобождения ресурса Y от task_b
#Получаем доступ к ресурсу X от task_a
#Выполняем работу с ресурсом X
    condition.notify_all() #Освобождаем ресурсы для всех задач
