import time
import sys

def Timer(sec):
    s = sec
    for i in range(sec):
        time.sleep(1)
        s -= 1
        sys.stdout.write(f'\rосталось ждать {time.strftime("%H:%M:%S", time.gmtime(s))}')
        sys.stdout.flush()
