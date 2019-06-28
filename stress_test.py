import os
import psutil
import numpy as np
import pysftp
import pyfastcopy
import datetime
import time
import re


def info(cpu_data, ram_data):
    # cpu = np.mean(cpu_data)
    cpu = cpu_data
    # print 'Cpu usage -', cpu, '%'
    # print 'Memory - min', min(ram_data), 'max', max(ram_data)
    # ram = max(ram_data) - min(ram_data)
    ram = np.mean(ram_data)
    # print 'Ram usage byte -', ram
    d_time = datetime.datetime.now().strftime('%H:%M:%S')
    print d_time, cpu, ram

    report = open('report.csv', 'a')    # Editing CSV report file
    report.write('\n{},{},{}'.format(d_time, cpu, ram))
    report.close()


def put_files(file):
    # print '\n--- put_files ---'
    # cpu_data = []
    ram_data = []
    file_list = os.listdir(r'incoming/')
    rang = 0
    if file_list:
        # print file_list[0]
        last_num = re.findall(r'\d+', file_list[0])
        rang = int(last_num[0])
        # print rang

    for i in range(rang + 1, rang + 801):
        name = 'file{}.xml'.format(i)
        pyfastcopy.copyfile(file, r'incoming/{}'.format(name))
        # cpu_data.append(psutil.cpu_percent())
        ram_data.append(psutil.virtual_memory().used)

    cpu_data = psutil.cpu_percent()
    info(cpu_data, ram_data)


def load_outgoing():
    print '\n--- load_outgoing ---'
    file_list = os.listdir(r'incoming/')
    file_list.reverse()
    cpu_data = []
    ram_data = []
    for i in file_list:
        pyfastcopy.copyfile(r'incoming/{}'.format(i), r'outgoing/{}'.format(i))
        cpu_data.append(psutil.cpu_percent())
        ram_data.append(psutil.virtual_memory().free)

    info(cpu_data, ram_data)
    return file_list


def remove_files(list_lst):
    print '\n--- remove_files ---'
    cpu_data = []
    ram_data = []
    for i in list_lst:
        cpu_data.append(psutil.cpu_percent())
        ram_data.append(psutil.virtual_memory().free)
        os.remove(r'outgoing/{}'.format(i))

    info(cpu_data, ram_data)


def connect():
    u_host = '192.168.1.182'
    u_user = 'user'
    u_pass = 'pass'
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=u_host, username=u_user, password=u_pass, cnopts=cnopts) as sftp:
        sftp.put(r'test.xml', r'/home/hich/incoming/t.xml')


f = open('report.csv', 'w')     # Creating of CSV report file
f.write('time,cpu_usage,ram_usage')
f.close()

for r in range(0, 900):
    put_files('test.xml')
    time.sleep(1)

# f_list = load_outgoing()
# remove_files(f_list)
# connect()

