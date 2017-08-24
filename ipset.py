#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import logging

fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO)

def ipset_basic_struct(action, ipset_name, ip):
    cmd = ['ipset', action]
    if not ipset_name:
        logging.error('no ipset name')
    cmd.append(ipset_name)
    if action != 'list' or action != 'flush' and not ipset_name:
		cmd.append(ip)

    process = subprocess.Popen(cmd, universal_newlines=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    returncode = process.poll()
    if returncode == 0:
        method = 'to' if action == 'add' else 'from'
        logging.info('%s %s %s ipset %s success' % (action, ip, method, ipset_name))
        return 0
    else:
        #logging.error(process.stderr.read())
        return 1

def ipset_add_ip(ipset_name, ip):
    return ipset_basic_struct('add', ipset_name, ip)

def ipset_del_ip(ipset_name, ip):
    return ipset_basic_struct('del', ipset_name, ip)

def ipset_check_ip(ipset_name, ip):
    return ipset_basic_struct('test', ipset_name, ip)
    
def ipset_check_set(ipset_name):
    return ipset_basic_struct('list', ipset_name, '')

def ipset_flush_set(ipset_name):
    return ipset_basic_struct('flush', ipset_name, '')

if __name__ == '__main__':
    ipset_add_ip('gfw', '8.8.8.8')
    ipset_del_ip('gfw', '8.8.8.8')
