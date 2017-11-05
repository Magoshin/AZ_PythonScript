#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import subprocess
import azGetVMList as VMList
import azGetVMPowerState as VMPwSts

AZCMD = "/root/bin/az"


def act_VMStart(vmName, resourceGroup):
    cmd0 = AZCMD + " vm start --resource-group " + resourceGroup
    cmd1 = " --name " + vmName
    cmd = cmd0 + cmd1
    proc = subprocess.call(cmd, shell=True)

    return proc


if __name__ == '__main__':
    # forceStartListを読み込んでおく
    forceStartList_Path = "/vortex/operator/forceStartList"
    ld = open(forceStartList_Path)
    lines = ld.readlines()

    msg = VMList.get_VMList()
    vm_dict = json.loads(msg)

    i = 0
    for x in vm_dict:
        status = VMPwSts.get_VMPowerState(vm_dict[i]['name'],
                                          vm_dict[i]['resourceGroup'])

        status_dict = json.loads(status)

        if status_dict['code'] != "PowerState/running":
            # forceStartList_Path をチェック
            for line in lines:
                if line.find(vm_dict[i]['name']) >= 0:
                    actres = act_VMStart(vm_dict[i]['name'],
                                         vm_dict[i]['resourceGroup'])
        i += 1
    # ファイルディスクリプタ閉じる
    ld.close()
