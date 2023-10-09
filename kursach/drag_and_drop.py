import tkinter as tk
import os
class DraggableLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.bind("<Button-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
        self._drag_data = {"x": 0, "y": 0}
        self._initial_position = {"x": 0, "y": 0}

    def on_drag_start(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self._initial_position["x"] = self.winfo_x()
        self._initial_position["y"] = self.winfo_y()

    def on_drag_motion(self, event):
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        self.place(x=self.winfo_x() + delta_x, y=self.winfo_y() + delta_y)
        

    def on_drag_release(self):
        self.place(x=self._initial_position["x"], y=self._initial_position["y"])
        overlapping_labels = self.find_overlapping_labels()
        if len(overlapping_labels) > 1:
            overlapping_labels.remove(self)
            self.drop(overlapping_labels)
        else:
            self.open()

    def find_overlapping_labels(self):
        overlapping_labels = []
        for label in self.master.children.values():
            if label != self and self.is_overlapping(label):
                overlapping_labels.append(label)
        return overlapping_labels

    def is_overlapping(self, other_label):
        x1, y1, x2 , y2= self.get_position()
        other_x1, other_y1, other_x2, other_y2 = other_label.get_position()
        return x1 < other_x2 and x2 > other_x1 and y1 < other_y2 and y2 > other_y1

    def get_position(self):
        x = self.winfo_x()
        y = self.winfo_y()
        width = self.winfo_width()
        height = self.winfo_height()
        return x, y, x + width, y + height

    def drop(self, overlapping_labels):
        print("Dropped on labels:", overlapping_labels)

    def open(self, event):
        elem = event.widget
        dir_name = elem["text"]
        fool_path = self.path_text.get() + dir_name
        if os.path.isdir(fool_path) and os.access(fool_path, os.R_OK):
            old_path = self.path_text.get()
            self.path_text.set(old_path + dir_name + '/')
            self.root_click('<Button-1>')
            self.refresh_window()

def check_drag_release(event):
    overlapping_labels = event.widget.find_overlapping_labels()
    if len(overlapping_labels) > 0:
        event.widget.drop(overlapping_labels)
    else:
        event.widget.open()

folder_name = DraggableLabel(self.inner_frame, text=item,  bg = 'white', cursor = 'hand1')
						#folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.bind("<ButtonRelease-1>", check_drag_release)

