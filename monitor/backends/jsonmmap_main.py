#!/usr/bin/python
# -*- coding: utf-8 -*-
import mmap
from jsonmmap import ObjectMmap
import random
import time

def main():
    mm = ObjectMmap(-1, 1024 * 1024, access=mmap.ACCESS_WRITE, tagname='share_mmap')
    while True:
        #length = random.randint(1, 100)
        #p = range(length)
        p = {'time':time.time()}
        mm.jsonwrite(p)
        print '*' * 30
        print mm.jsonread_master()
        time.sleep(3)


if __name__ == '__main__':
    main()