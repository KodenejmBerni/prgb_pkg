import threading as thd
from time import sleep
from typing import Iterable

from prgb_pkg.prgb_window import PrgbWindow


class Prgb:
    instance = None
    version = 0.1

    def __new__(cls, source_container: Iterable):
        if cls.instance is None:
            o = super().__new__(cls)
            o.window_thread = None
            cls.instance = o
        return cls.instance

    def __init__(self, source_container: Iterable):
        window_thread_name = 'prgb_window_thread'

        self.new_iter = iter(source_container)
        if self.window_thread is None:
            self.add_subbar_event = thd.Event()
            self.remove_subbar_event = thd.Event()
            self.sync_lock = thd.Lock()
            self.subbars_amount = 0
            self.window_thread = thd.Thread(target=self.run_window, name=window_thread_name)
            self.window_thread.start()
        elif not self.window_thread.is_alive():
            self.window_thread = thd.Thread(target=self.run_window, name=window_thread_name)
            self.window_thread.start()

    def __iter__(self):
        self.add_subbar_event.set()
        self.sync_lock.acquire()
        self.sync_lock.acquire()
        self.subbars_amount += 1
        return PrgbIter(self)

    def run_window(self):
        window = PrgbWindow(
            self.add_subbar_event,
            self.remove_subbar_event,
            self.sync_lock,
        )
        window.mainloop()


class PrgbIter:
    def __init__(self, prgb_obj: Prgb):
        self.prgb_obj = prgb_obj
        self.iter = self.prgb_obj.new_iter

    def __next__(self):
        # TODO Prgb calculations
        try:
            return next(self.iter)
        except StopIteration:
            self.prgb_obj.remove_subbar_event.set()
            self.prgb_obj.sync_lock.acquire()
            self.prgb_obj.sync_lock.acquire()
            self.prgb_obj.subbars_amount -= 1
            sleep(.02)
            raise StopIteration
