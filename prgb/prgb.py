import threading as thd

from prgb.prgb_window import PrgbWindow


class PrgbIter:
    def __init__(self, source_container_iter):
        self.source_container_iter = source_container_iter

    def __next__(self):
        # TODO Prgb calculations
        try:
            return next(self.source_container_iter)
        except StopIteration:
            Prgb.remove_subbar_event.set()
            Prgb.sync_lock.acquire()
            Prgb.sync_lock.acquire()
            Prgb.subbars_amount -= 1
            # if not Prgb.subbars_amount:
            #     Prgb._window_thread.join()
            raise StopIteration


class Prgb:
    _instance = None
    add_subbar_event = thd.Event()
    remove_subbar_event = thd.Event()
    sync_lock = thd.Lock()
    subbars_amount = 0

    def __new__(cls, source_container):
        cls._source_container_iter = iter(source_container)
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._window_thread = thd.Thread(target=cls.run_window)
            cls._window_thread.start()
        if not cls._window_thread.is_alive():
            cls._window_thread = thd.Thread(target=cls.run_window)
            cls._window_thread.start()
        return cls._instance

    def __iter__(self):
        self.add_subbar_event.set()
        self.sync_lock.acquire()
        self.sync_lock.acquire()
        self.subbars_amount += 1
        return PrgbIter(self._source_container_iter)

    @classmethod
    def run_window(cls):
        window = PrgbWindow(cls.add_subbar_event, cls.remove_subbar_event, cls.sync_lock)
        window.mainloop()
