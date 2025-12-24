# -*- coding: utf-8 -*-
#创建时间：2025/11/3 18:09

from project.data_parse.time_parse import time_parse
def read_sensor_addr_info():
    with open('../info_addr/sensor_addr_info.txt', 'r') as f:
        s = f.read()
        sensor_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 传感器地址所组成的列表
    return sensor_list

def read_power_addr_info():
    with open('../info_addr/power_addr_info.txt', 'r') as f:
        s = f.read()
        power_list= [s[i:i + 2] for i in range(0, len(s), 2)]  # 电表地址所组成的列表
    return power_list

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
sensor_timing_var={}
def read_sensor_timing():   #{'15': 'DDEEFF15080017007F01', '22': 'DDEEFF22080017007F01',...}
    with open('../info_addr/sensor_addr_info.txt', 'r') as f:
        s = f.read()
        sensor_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 传感器地址所组成的列表
        sensor_read_info_name_list = ['read_info_' + i for i in sensor_list]    #[read_info_15,read_info_16,...]
        for read_info_name in sensor_read_info_name_list:
            with open(f'../info_timing/{read_info_name[5:]}.txt') as f:
                info = f.read()
            sensor_timing_var[read_info_name[-2:]]=info
    return sensor_timing_var


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def read_power_timing():   #{'79': 'DDEEFF15080017007F01', '7A': 'DDEEFF22080017007F01',...}
    power_timing_var={}
    with open('../info_addr/power_addr_info.txt', 'r') as f:
        s = f.read()
        power_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 电表地址所组成的列表
        power_read_info_name_list = ['read_info_' + i for i in power_list]    #[read_info_79,read_info_7A,...]
        for read_info_name in power_read_info_name_list:
            with open(f'../info_timing/{read_info_name[5:]}.txt') as f:
                info = f.read()
            power_timing_var[read_info_name[-2:]]=info
    return power_timing_var


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def read_info_06():
    with open('../info_timing/info_06.txt') as f:
        info_06 = f.read()
    f.close()
    return info_06


def write_info(addr, command):
    """
    :param addr: 地址，可以是整数（15, 16）或字符串（'7A', '79'）
    :param command: 要写入的命令字符串
    """
    filename = f"../info_timing/info_{addr}.txt"
    with open(filename, 'w') as f:
        f.write(command)


def write_info_06(command):
    with open('../info_timing/info_06.txt', 'w') as f:
        f.write(command)

def str_into_hex(x):
    sorted_int = sorted(map(int, set(x)), reverse=True)
    str = '0'
    for i in range(7, 0, -1):
        if i not in sorted_int:
            str += '0'
        else:
            str += '1'
    return hex(int(str, 2)).upper()[2:]

'''管理员设置定时数据，将这些数据转换成原始数据'''
def change_into_command(workday, begin_hour, begin_minute, end_hour, end_minute, interval):
    '''
    str1:起始小时   str2：起始分钟
    str3:结束小时   str4：结束分钟
    str5：工作日    str6：间隔
    '''
    str1=hex(int(begin_hour)).upper()[2:]
    if len(str1) == 1:str1='0' + str1

    str2=hex(int(begin_minute)).upper()[2:]
    if len(str2) == 1: str2 = '0' + str2

    str3 = hex(int(end_hour)).upper()[2:]
    if len(str3) == 1: str3 = '0' + str3

    str4 = hex(int(end_minute)).upper()[2:]
    if len(str4) == 1: str4 = '0' + str4

    str5 = str_into_hex(workday)
    if len(str5)==1:str5 = '0' + str5

    str6 = hex(int(interval)).upper()[2:]
    if len(str6) == 1: str6 = '0' + str6

    return str1+str2+str3+str4+str5+str6

def get_timing_data():  #'''读取所有节点的定时信息'''
    timing_data=[]#存放所有节点的定时信息

    sensor_list = read_sensor_addr_info()
    timing_data_var={}

    power_list = read_power_addr_info()
    timing_power_data_var = {}

#获取传感器的定时数据
    for read_info_name in sensor_list:
        info=read_sensor_timing()[read_info_name]
        if info != '':
            timing_data_xx = time_parse(info)
            timing_data.append(timing_data_xx)
            timing_data_var[read_info_name[-2:]] = timing_data_xx
        else:
            timing_data.append('')
            timing_data_var[read_info_name[-2:]] = ''
# 获取电表的定时数据
    for read_info_name in power_list:
        info=read_power_timing()[read_info_name]
        if info != '':
            timing_data_xx = time_parse(info)
            timing_data.append(timing_data_xx)
            timing_power_data_var[read_info_name[-2:]] = timing_data_xx
        else:
            timing_data.append('')
            timing_power_data_var[read_info_name[-2:]] = ''

    #06
    info_06 = read_info_06()
    if info_06 != '':
        timing_data_06 = time_parse(info_06)
        timing_data.append(timing_data_06)
    else:timing_data.append('')

    return timing_data,timing_data_var,timing_power_data_var

def get_timing_str():
    info_workday=[]
    timing_data = get_timing_data()[0]
    sensor_timing = read_sensor_timing()
    for addr in read_sensor_addr_info():
        workday=sensor_timing[addr][-4:-2]
        info_workday.append(workday)
    power_timing = read_power_timing()
    for addr in read_power_addr_info():
        workday = power_timing[addr][-4:-2]
        info_workday.append(workday)
    info_06_workday = read_info_06()[-4:-2]
    info_workday.append(info_06_workday)

    addr_list=[addr for addr in read_sensor_addr_info()]+[addr for addr in read_power_addr_info()]
    flag=True
    code=[]
    for addr in addr_list:
        if(flag):
            code.append('B'+addr)
            flag=False
            continue
        code.append('A'+addr)
    code.append('A06')


    server_data = []
    count_out = 0
    workday_index=0
    for every_timing in timing_data:
        count_in = 0
        server_data.append(str(code[count_out]))
        count_out += 1
        for every_set in every_timing:
            if count_in == 4:  # 处理集合
                count_in += 1
                server_data.append(info_workday[workday_index])
                workday_index+=1
                continue
            count_in += 1
            server_data.append(str(every_set))
    server_data = ' '.join(server_data)
    return server_data

if __name__ == '__main__':

    print(read_sensor_addr_info())


