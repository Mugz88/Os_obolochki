import threading
import time
class TaskA(threading.Thread):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self._lock = threading.Lock()
    def run(self):
        while True:
            with self._lock:
                print(f"TaskA: {self.x} {self.y}")
                time.sleep(1)
class TaskB(threading.Thread):
    def __init__(self, x):
        super().__init__()
        self.x = x
    def run(self):
        with self.x:
            print("TaskB: X")
            time.sleep(2)
            self.join()
if __name__ == "__main__":
    #Создаем две задачи с разными приоритетами
    task_a = TaskA('X', 'Y')
    task_b = TaskB('Y')
    #Запускаем задачи
    task_a.start()
    task_b.start()
    #Ждем завершения задач
    task_a.join()
    task_b.join()