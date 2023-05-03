# main.py -- put your code here!
import os
import struct

def randint(min = 0, max = 65535):
    diff = max - min
    val = struct.unpack('H', os.urandom(2))[0] % diff
    return val + min

x = 0
while x < 15:
    num = randint(1000, 156062)
    print('num is')
    print(num)
    # print('random num is: ')
    # print()
    x += 1


     # k = 2
     # while(contador > k):
     #      k += 1
     #      data2 += 'a'