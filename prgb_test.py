from time import sleep

from prgb_pkg.prgb import Prgb

list1 = [1, 2, 3]
dict1 = {'a': 10, 'b': 20, 'c': 30}

for x in Prgb(list1):
    print(x)
    for k, v in Prgb(dict1.items()):
        print(f'{x}.{k}: {v}')
        sleep(.5)
    sleep(.5)
sleep(.5)

for x in Prgb(list1):
    print(x)
    for k, v in Prgb(dict1.items()):
        print(f'{x}.{k}: {v}')
        sleep(.5)
    sleep(.5)
sleep(.5)
