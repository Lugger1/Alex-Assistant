# Python program raising
# exceptions in a python
# thread

import threading
import ctypes
import time

list_threads = []

class thread_with_exception(threading.Thread):
    def __init__(self, func, args=None, name='Thread', repeats=1):
        threading.Thread.__init__(self)
        list_threads.append(self)
        self.list_pos = len(list_threads)-1
        self.func = func
        self.args = args
        self.name = name
        self.repeats = repeats
    
    def run(self):
        print(f'поток "{self.name}" запущен')
        # target function of the thread class
        for i in range(self.repeats):
            try: self.func(self.args)
            except TypeError:
                self.func()
        
        try:
            list_threads.pop(self.list_pos)
        except IndexError:
            pass
        
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
            ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
        
        print(f'поток \"{self.name}\" с кодом {thread_id} закрыт')

if __name__ == "__main__":
    t1 = thread_with_exception(func=lambda: print('Thread 1'))
    t1.start()
    time.sleep(2)
    t1.raise_exception()
    t1.join()
