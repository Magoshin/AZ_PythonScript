#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import subprocess

AZCMD = "/root/bin/az"


def get_VMPowerState(vmName, resourceGroup):
    cmd0 = AZCMD + " vm get-instance-view --name " + vmName
    cmd1 = " --resource-group " + resourceGroup
    cmd2 = " --query instanceView.statuses[1] --output json"

    cmd = cmd0 + cmd1 + cmd2

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
