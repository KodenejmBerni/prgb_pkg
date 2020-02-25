from time import sleep

from prgb_pkg.prgb import Prgb

dict1 = {'a': 10, 'b': 20, 'c': 30}

for x in Prgb(range(3)):
    # print(x)
    for k, v in Prgb(dict1.items()):
        print(f'{x}.{k}: {v}')
        sleep(1)

for x in Prgb(range(3)):
    # print(x)
    for k, v in Prgb(dict1.items()):
        print(f'{x}.{k}: {v}')
        sleep(1)
