#!/usr/bin/python
# -*- coding: utf-8 -*-
import mmap
from jsonmmap import ObjectMmap
import time


def main():
    mm = ObjectMmap(-1, 1024 * 1024, access=mmap.ACCESS_READ, tagname='share_mmap')
    while True:
        last_data = mm.jsonread_follower()
        if mm.jsonread_follower() != last_data:
            print '*' * 30
            print mm.jsonread_follower()
        print '-' * 30
        print mm.jsonread_follower()


if __name__ == '__main__':
    main()