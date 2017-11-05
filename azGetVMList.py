#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import subprocess

AZCMD = "/root/bin/az"


# Functions
def get_VMList():

    cmd = AZCMD + " vm list"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    buf = []

    while True:
        # バッファから1行読み込む.
        line = proc.stdout.readline()
        buf.append(line)
        sys.stdout.write(line)

        # バッファが空 + プロセス終了.
        if not line and proc.poll() is not None:
            break

    return ''.join(buf)
