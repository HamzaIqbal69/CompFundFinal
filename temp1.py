import sys
import select
from time import sleep

mess = str()
print('Enter something: ',end = '',flush=True)

while True:
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        c = sys.stdin.read(1)
        if c == '\n':
            break
        else:
            mess += c
            sleep(.001)

print(mess)