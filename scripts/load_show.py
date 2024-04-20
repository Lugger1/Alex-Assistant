import time
import sys

status = True

def show_load():
    global status
    while status:
        for i in range(10):
            time.sleep(0.2)
            i = str(i); i = list(i)
            if i[-1] == '0' or i[-1] == '4' or i[-1] == '8' and status:
                sys.stdout.write(f"\r\\")
                continue
            elif i[-1] == '1' or i[-1] == '5' or i[-1] == '9' and status:
                sys.stdout.write(f"\r|")
                continue
            elif i[-1] == '2' or i[-1] == '6' and status:
                sys.stdout.write(f"\r/")
                continue
            elif i[-1] == '3' or i[-1] == '7' and status:
                sys.stdout.write(f"\r-")
                continue
            
            sys.stdout.flush()
    else:
        sys.stdout.write('Sucсess!\n')
        sys.stdout.flush()
        status = True
        return
