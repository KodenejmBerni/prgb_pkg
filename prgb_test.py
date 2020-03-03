from time import sleep

from prgb_pkg import Prgb

dict1 = {'a': 10, 'b': 20, 'c': 30, 'd': 40}

for x in Prgb((i for i in range(3)), 'Range bar'):
    print(x)
    for k, v in Prgb(dict1.items(), 'Dict bar', print_summary=True):
        for i in Prgb(range(3), '3rd deep'):
            print(f'{x}.{k}: {v}')
            dict1[k] = v + 1
            sleep(.5)
