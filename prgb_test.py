from prgb.prgb import Prgb
from time import sleep

list1 = [1, 2, 3]
dict1 = {'a': 10, 'b': 20, 'c': 30}

for x in Prgb(list1):
    print(x)
    for k, v in Prgb(dict1.items()):
        print(f'{x}.{k}: {v}')
        # sleep(.5)
    sleep(.5)

sleep(1)
for k, v in Prgb(dict1.items()):
    print(f'.{k}: {v}')
    sleep(.5)
