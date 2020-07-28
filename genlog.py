#!/usr/bin/env python3
#
# docker log format
# {
#   "log": "...",
#   "stream": "stdout",
#   "time": "2020-07-28T10:23:56.183733788Z"
# }
#
import random
import string
import json
import time
import os
import sys
from datetime import datetime

os.environ['TZ'] = 'UTC'

def random_str(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def write_log(length):
    log = {
      'log': random_str(length),
      'stream': 'stdout',
      'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f000Z')
    }
    print(json.dumps(log))


if __name__ == '__main__':
    generate_lines = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
    for i in range(generate_lines):
        write_log(random.randint(800, 16000))
