#!/usr/bin/env python3
import time
import sys

i = 0
for line in sys.stdin:
    print(line, end='')
    if i % 100 == 0:
        time.sleep(0.1)
    i += 1
