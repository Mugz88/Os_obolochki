import threading
def task_a():
    while True:
#Выполнение задачи A
        if is_blocked_a:
            print("Task A blocked resource X and is waiting")
        return
#Получение доступа к ресурсу X
    resource_x.acquire()
#Выполнение работы с ресурсом X
#Освобождение ресурса X
    resource_x.release()
def task_b():
    while True:
#Выполнение задачи B
        if is_blocked_b:
            print("Task B blocked resource Y and is waiting")
            return
Получение доступа к ресурсу Y
resource_y.acquire()
Выполнение работы с ресурсом Y
Освобождение ресурса Y
resource_y.release()


def check_mutual_blocking():
Проверка взаимной блокировки для задач A и B
if (is_blocked_a and not is_blocked_b):
print("Task A is blocking resource X and cannot proceed")
return False
elif (is_blocked_b and not is_blocked_a):
print("Task B is blocking resource Y and cannot proceed")
return False
else:
return True
