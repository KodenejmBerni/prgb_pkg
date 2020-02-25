import threading as thd
from time import sleep
from typing import Iterable

from prgb_pkg.decorators import if_window_still_requested
from prgb_pkg.prgb_window import PrgbWindow


class Prgb:
    version = 0.1
    instance = None

    def __new__(cls, source_container: Iterable, title=''):
        if cls.instance is None:
            o = super().__new__(cls)
            o.window_thread = None
            cls.instance = o
        return cls.instance

    def __init__(self, source_container: Iterable, title=''):
        window_thread_name = 'prgb_window_thread'
        self.current_title = title
        self.current_iter = iter(source_container)
        if self.window_thread is None:
            self.add_subbar_event = thd.Event()
            self.remove_subbar_event = thd.Event()
            self.no_window_request = thd.Event()
            self.sync_lock = thd.Lock()
            self.subbars_amount = 0
            self.window_thread = thd.Thread(target=self.run_window, name=window_thread_name)
            self.window_thread.start()
        elif not self.window_thread.is_alive() and not self.no_window_request.is_set():
            self.window_thread = thd.Thread(target=self.run_window, name=window_thread_name)
            self.window_thread.start()

    def __iter__(self):
        self.send_signal_add_subbar()
        self.subbars_amount += 1
        return PrgbIter(self)

    def run_window(self):
        window = PrgbWindow(self)
        window.mainloop()

    @if_window_still_requested
    def send_signal_add_subbar(self):
        self.add_subbar_event.set()
        self.sync_lock.acquire()
        self.sync_lock.acquire()
        sleep(PrgbWindow.CHECK_EVENTS_REFRESH_RATE_ms * 2 / 1000)

    @if_window_still_requested
    def send_signal_remove_subbar(self):
        self.remove_subbar_event.set()
        self.sync_lock.acquire()
        self.sync_lock.acquire()
        sleep(PrgbWindow.CHECK_EVENTS_REFRESH_RATE_ms * 2 / 1000)


class PrgbIter:
    def __init__(self, prgb_obj: Prgb):
        self.prgb_obj = prgb_obj
        self.iter = self.prgb_obj.current_iter

    def __next__(self):
        # TODO Prgb calculations
        try:
            return next(self.iter)
        except StopIteration:
            self.prgb_obj.send_signal_remove_subbar()
            self.prgb_obj.subbars_amount -= 1
            raise StopIteration
