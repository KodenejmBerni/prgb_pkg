import tkinter as tk
from tkinter import ttk


class PrgbWindow(tk.Tk):
    CHECK_EVENTS_REFRESH_RATE_ms = 10

    def __init__(self, prgb_obj):
        super().__init__()
        self.prgb_obj = prgb_obj

        self.title(f'Prgb v{self.prgb_obj.version}')
        self.minsize(300, 100)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.geometry('300x300')
        # self.iconbitmap()
        self.subbars_container = tk.Frame(self)
        self.subbars_container.pack(fill=tk.X, expand=1, anchor=tk.N)

    def add_subbar(self):
        title = self.prgb_obj.current_title
        subbar_frame = tk.Frame(self.subbars_container, relief=tk.RAISED, bd=3, height=100)
        subbar_frame.pack(fill=tk.X, expand=1)
        subbar_title = tk.Label(subbar_frame, text=title)
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
        if self.prgb_obj.sync_lock.locked():
            if self.prgb_obj.add_subbar_event.isSet():
                self.add_subbar()
                self.prgb_obj.add_subbar_event.clear()
            if self.prgb_obj.remove_subbar_event.isSet():
                self.remove_subbar()
                self.prgb_obj.remove_subbar_event.clear()
            self.prgb_obj.sync_lock.release()
        if not self.prgb_obj.no_window_request.is_set():
            self.after(self.CHECK_EVENTS_REFRESH_RATE_ms, self.check_events)

    def mainloop(self, n=0):
        self.check_events()
        self.attributes('-topmost', True)
        self.update()
        self.attributes('-topmost', False)
        super().mainloop(n)

    def on_closing(self):
        self.prgb_obj.no_window_request.set()
        self.prgb_obj.add_subbar_event.clear()
        self.prgb_obj.remove_subbar_event.clear()
        if self.prgb_obj.sync_lock.locked():
            self.prgb_obj.sync_lock.release()
        self.destroy()
