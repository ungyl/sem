# -*- coding: utf-8 -*-
#创建时间：2025/9/20 11:16
import os
import re
import socket
import threading

from project.client_server import connect_server
from project.create_table import create_table
from project.data_parse.relay_parse import send_relay_change_state
from project.get_data import get_data, data_parse
from project.read_write_info import *

'''
    1.立即查询：数据库中存放的最新数据
    2.定时设置，目前到点 获得数据库中存放的最新数据。每个节点分开定时，到点就将节点最新数据存在数据库中。最新数据刷新界面
            
'''
timing_state_15=False
timing_state_16=False
timing_state_79=False
timing_state_7A=False
timing_state_06=False


def handle_client(conn, addr):
    """负责与单个客户端对话"""
    print('[Server] 客户端接入:', addr)
    while True:
        sensor_addr_list = read_sensor_addr_info()      #方便后续判断 设备是否存在
        power_addr_list = read_power_addr_info()

        info = conn.recv(1024).hex().upper()#客户端发来的数据
        print(info)
        if not info or info == 'BYE':
            break

        '''操作设置命令'''
        global timing_state_15
        global timing_state_16
        global timing_state_79
        global timing_state_7A
        global timing_state_06

        if info=='DDEEFF0A11':   #请求获得每个节点的定时信息
            timing_data=get_timing_str()
            conn.send(timing_data.encode('utf-8'))

        elif len(info)==8 and info[0:6] == 'DDEEFF' and info[6:8] in (sensor_addr_list+power_addr_list+['06']):#根据addr获取相应的定时数据
            timing_data = get_timing_str()#全部节点的定时信息
            m = re.search(rf'\b[AB]{re.escape(info[6:8])}\b', timing_data)
            start = m.start()
            next_block = re.search(r'[AB]\d+', timing_data[start + 1:])
            end = next_block.start() + start + 1 if next_block else len(timing_data)
            conn.send(timing_data[start:end].strip().encode('utf-8'))

        elif info[:14]=='06100102000408' and len(info)==34:#改变继电器状态
            connect_server(info)#将info这个命令转发
            #立即获得继电器状态，并存储到数据库中
            data_parse(['0603010000018441'])

            server_data=send_relay_change_state(info)#哪几路开，哪几路关
            conn.send(server_data.encode('utf-8'))

        else:
            if info[:6]=='AABBCC':
                if info[-2:]=='03':#'''立即查询(将实时数据存储在数据库中，再拿出)'''
                    if info[6:8] == '15': data_parse(['150300000002C71F'])
                    elif info[6:8] == '16': data_parse(['160300000002C72C'])
                    elif info[6:8] == '79': data_parse(['79032000001045BE', '790340000006DA70'])
                    elif info[6:8] == '7A': data_parse(['7A0320000010458D', '7A0340000006DA43'])
                    elif info[6:8] == '06': data_parse(['0603010000018441'])
                    humiture_15,humiture_16,power_79,power_7A,relay = pull_data_from_database()
                    server_data = {
                        'AABBCC1503': 'A15 '+humiture_15,
                        'AABBCC1603': 'A16 '+humiture_16,
                        'AABBCC7903': 'A79 '+power_79,
                        'AABBCC7A03': '7A '+power_7A,
                        'AABBCC0603': 'A06 '+relay,
                    }.get(info, 'ERR')
                    conn.send(server_data.encode('utf-8'))

                elif info[-2:]=='55':#'''激活自动查询'''
                    activate_info=info[6:8]
                    if activate_info=='15':timing_state_15 = True
                    elif activate_info=='16':timing_state_16 = True
                    elif activate_info == '79':timing_state_79 = True
                    elif activate_info == '7A': timing_state_7A = True
                    elif activate_info == '06': timing_state_06 = True
                    server_data = {
                        'AABBCC1555': 'activate 15 successfully',
                        'AABBCC1655': 'activate 16 successfully',
                        'AABBCC7955': 'activate 79 successfully',
                        'AABBCC7A55': 'activate 7A successfully',
                        'AABBCC0655': 'activate 06 successfully',
                    }.get(info, 'ERR')
                    conn.send(server_data.encode('utf-8'))

                elif info[-2:]=='AA':#'''禁止自动查询'''
                    prohibit_info = info[6:8]
                    if prohibit_info=='15':
                        timing_state_15 = False
                        open('../info_timing/info_15.txt', 'w').close()
                    elif prohibit_info=='16':
                        timing_state_16 = False
                        open('../info_timing/info_16.txt', 'w').close()
                    elif prohibit_info == '79':
                        timing_state_79 = False
                        open('../info_timing/info_79.txt', 'w').close()
                    elif prohibit_info == '7A':
                        timing_state_7A = False
                        open('../info_timing/info_7A.txt', 'w').close()
                    elif prohibit_info == '06':
                        timing_state_06 = False
                        open('../info_timing/info_06.txt', 'w').close()
                    server_data = {
                        'AABBCC15AA': 'prohibit 15 successfully',
                        'AABBCC16AA': 'prohibit 16 successfully',
                        'AABBCC79AA': 'prohibit 79 successfully',
                        'AABBCC7AAA': 'prohibit 7A successfully',
                        'AABBCC06AA': 'prohibit 06 successfully',
                    }.get(info, 'ERR')
                    conn.send(server_data.encode('utf-8'))
                else:conn.send('ERR'.encode('utf-8'))

            elif info[:6]=='BBCCDD':#增加传感器设备
                addr=info[6:8]
                #1.检查addr是否在sensor_addr_info.txt中
                sensor_addr_list=read_sensor_addr_info()
                #2.不存在，则添加；存在，则返回已存在
                if addr not in sensor_addr_list:
                    with open('../info_addr/sensor_addr_info.txt', 'a') as f:  # 追加
                        f.write(addr)
                    create_table()  # 设备添加成功后，创建表
                    # 3.生成info_addr.txt,方便后续写入定时命令
                    open(f'../info_timing/info_{addr}.txt', 'w').close()
                    conn.send(f'add {addr} successfully'.encode('utf-8'))
                else:conn.send(f'{addr} already exists'.encode('utf-8'))

            elif info[:6]=='CCBBDD':#删除传感器设备
                addr = info[6:8]
                # 1.检查addr是否在sensor_addr_info.txt中
                with open('../info_addr/sensor_addr_info.txt', 'r') as f:
                    s = f.read()
                    sensor_addr_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 传感器地址所组成的列表
                # 2.存在，则删除；不存在，则返回不存在
                if addr in sensor_addr_list:
                    with open('../info_addr/sensor_addr_info.txt', 'w') as f:  # 覆盖
                        f.write(s.replace(addr, ''))
                    # 3.删除info_addr.txt
                    os.remove(f'../info_timing/info_{addr}.txt')
                    conn.send(f'delete {addr} successfully'.encode('utf-8'))
                else:conn.send(f'{addr} does not exist'.encode('utf-8'))

            elif info[:6]=='CCDDEE':#增加电表设备
                addr = info[6:8]
                # 1.检查addr是否在sensor_addr_info.txt中
                power_addr_list = read_power_addr_info()
                # 2.不存在，则添加；存在，则返回已存在
                if addr not in power_addr_list:
                    with open('../info_addr/power_addr_info.txt', 'a') as f:  # 追加
                        f.write(addr)
                    create_table()  # 设备添加成功后，创建表
                    # 3.生成info_addr.txt,方便后续写入定时命令
                    open(f'../info_timing/info_{addr}.txt', 'w').close()
                    conn.send(f'add {addr} successfully'.encode('utf-8'))
                else:conn.send(f'{addr} already exists'.encode('utf-8'))

            elif info[:6]=='DDCCEE':#删除电表设备
                addr = info[6:8]
                # 1.检查addr是否在sensor_addr_info.txt中
                with open('../info_addr/power_addr_info.txt', 'r') as f:
                    s = f.read()
                    power_addr_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 传感器地址所组成的列表
                # 2.存在，则删除；不存在，则返回不存在
                if addr in power_addr_list:
                    with open('../info_addr/power_addr_info.txt', 'w') as f:  # 覆盖
                        f.write(s.replace(addr, ''))
                    # 3.删除info_addr.txt
                    if os.path.exists(f'../info_timing/info_{addr}.txt'):
                        os.remove(f'../info_timing/info_{addr}.txt')
                    conn.send(f'delete {addr} successfully'.encode('utf-8'))
                else:conn.send(f'{addr} does not exist'.encode('utf-8'))

            elif info[:6]=='DDEEFF':#'''定时设置命令'''
                addr=info[6:8]
                sensor_and_power_addr_list=read_sensor_addr_info()+read_power_addr_info()+['06']
                if addr not in sensor_and_power_addr_list:
                    conn.send('ERR'.encode('utf-8'))#'''请求命令非法'''

                else:#'''请求命令合法，根据addr向对应文件中写入定时命令'''
                    # 06
                    if addr == '06':
                        if timing_state_06:
                            threading.Thread(target=write_info_06, args=(info,), daemon=True).start()
                            conn.send('timing06_OK'.encode('utf-8'))
                        else:conn.send('timing06 is in prohibited'.encode('utf-8'))
                        continue
                    #传感器、电表
                    if(addr not in ['15','16','79','7A']):#添加的设备，则允许定时-------便于测试
                        globals()[f'timing_state_{addr}']= True
                    if globals()[f'timing_state_{addr}']:
                        threading.Thread(target=write_info, args=(addr,info), daemon=True).start()
                        conn.send(f'timing{addr}_OK'.encode('utf-8'))
                    else:conn.send(f'timing{addr} is in prohibited'.encode('utf-8'))

            else:conn.send('ERR'.encode('utf-8'))

    conn.close()
    print('[Server] 客户端断开:', addr)

def esp32_server():
    """永久监听，线程入口"""
    with socket.socket() as sock:#自动关闭
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#允许地址复用
        sock.bind(('0.0.0.0', 8888))#绑定
        sock.listen(5)#监听
        print('[Server] 已在后台线程监听 8888 ...')
        while True:
            conn, addr = sock.accept()#等待客户连接
            # 简单写法：再开一条子线程处理这个客户端
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
def pull_data_from_database():
    # 实时拉取数据库中最新数据
    data      = get_data()[0]
    data[0]=data[0][:-1]
    data[1]=data[1][:-1]#只要数值，不要单位
    humiture_15 = ' '.join(data[:2])

    data[2] = data[2][:-1]
    data[3] = data[3][:-1]
    humiture_16 = ' '.join(data[2:4])

    data[4] = data[4][:-1]
    # data[5] = data[5][:-1]    电流
    # data[6] = data[6][:-1]    功率
    data[7] = data[7][:-3]
    power_79    = ' '.join([data[4],data[7]])

    data[8] = data[8][:-1]
    # data[9] = data[9][:-1]
    # data[10] = data[10][:-1]
    data[11] = data[11][:-3]
    power_7A    = ' '.join([data[8],data[11]])

    relay       = ''.join(data[12]).replace('开','1').replace('关','0')
    return humiture_15,humiture_16,power_79,power_7A,relay

if __name__ == '__main__':
    esp32_server()
