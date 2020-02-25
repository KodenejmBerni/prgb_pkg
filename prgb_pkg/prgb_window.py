import tkinter as tk
from tkinter import ttk


class PrgbWindow(tk.Tk):
    def __init__(self, add_subbar_event, remove_subbar_event, sync_lock):
        super().__init__()
        self.add_subbar_event = add_subbar_event
        self.remove_subbar_event = remove_subbar_event
        self.sync_lock = sync_lock

        self.title('Prgb')
        self.minsize(300, 100)
        # self.geometry('300x300')
        # self.iconbitmap()
        self.subbars_container = tk.Frame(self)
        self.subbars_container.pack(fill=tk.X, expand=1, anchor=tk.N)

    def add_subbar(self):
        subbar_frame = tk.Frame(self.subbars_container, relief=tk.RAISED, bd=3, height=100)
        subbar_frame.pack(fill=tk.X, expand=1)
        subbar_title = tk.Label(subbar_frame, text='Progress bar title')
        subbar_title.pack(pady=(10, 5))
        progress_bar = ttk.Progressbar(subbar_frame)
        progress_bar.pack(fill=tk.X, expand=1, padx=15)
        subbar_info = tk.Label(subbar_frame, text='examples info')
        subbar_info.pack(pady=(5, 10), padx=15, anchor=tk.NE)

    def remove_subbar(self):
        children = list(self.subbars_container.children.values())
        children[-1].destroy()
        if len(children) == 1:
            self.destroy()

    def check_events(self):
        if self.sync_lock.locked():
            if self.add_subbar_event.isSet():
                self.add_subbar()
                self.add_subbar_event.clear()
            if self.remove_subbar_event.isSet():
                self.remove_subbar()
                self.remove_subbar_event.clear()
            self.sync_lock.release()
        self.after(10, self.check_events)

    def mainloop(self, n=0):
        self.check_events()
        super().mainloop(n)
