#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import subprocess
import azGetVMList as VMList
import azGetVMPowerState as VMPwSts

AZCMD = "/root/bin/az"


# Functions
def act_VMDeallocate(vmName, resourceGroup):
    cmd0 = AZCMD + " vm deallocate --resource-group " + resourceGroup
    cmd1 = " --name " + vmName
    cmd = cmd0 + cmd1
    proc = subprocess.call(cmd, shell=True)

    return proc


if __name__ == '__main__':

    # persistentStartList$B$rFI$_9~$s$G$*$/(B
    persistentStartList_Path = "/vortex/operator/persistentStartList"
    ld = open(persistentStartList_Path)
    lines = ld.readlines()

    msg = VMList.get_VMList()
    vm_dict = json.loads(msg)

    i = 0
    for x in vm_dict:
        status = VMPwSts.get_VMPowerState(vm_dict[i]['name'],
                                  vm_dict[i]['resourceGroup'])
        status_dict = json.loads(status)

        if status_dict['code'] == "PowerState/running":
            # persistentStartList $B$r%A%'%C%/(B
            for line in lines:
                if line.find(vm_dict[i]['name']) < 0:
                    actres = act_VMDeallocate(vm_dict[i]['name'],
                                              vm_dict[i]['resourceGroup'])
        i += 1

    # $B%U%!%$%k%G%#%9%/%j%W%?JD$8$k(B
    ld.close()
