import tkinter as tk

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack()

        self.pat_text = tk.StringVar(value="Начальный текст")

        self.current_path = tk.Entry(self.title_frame, textvariable=self.pat_text, width=80, state='readonly')
        self.current_path.pack()

        self.button = tk.Button(self.title_frame, text="Открыть второе окно", command=self.open_second_window)
        self.button.pack()

        self.root.mainloop()

    def open_second_window(self):
        second_window = tk.Toplevel(self.root)
        second_label = tk.Label(second_window, textvariable=self.pat_text)
        second_label.pack()

        new_text = "Новый текст"
        self.pat_text.set(new_text)

app = MyApp()