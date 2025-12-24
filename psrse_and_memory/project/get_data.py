# -*- coding: utf-8 -*-
#创建时间：2025/9/3 23:17 
from project.client_server import connect_server
from project.data_parse.current_and_power_parse import get_current_power
from project.data_parse.electric_energy_parse import get_electric_energy
from project.data_parse.humiture_parse import get_humiture
from project.data_parse.relay_parse import check_relay_state, change_relay_state
from project.database_configure import database_configure
from project.read_write_info import read_sensor_addr_info, read_power_addr_info

'''
    1.发送对应节点的client_reqs后，获得数据并存在数据库中对应表中
    2.提供数据库中最新数据data
'''

'''data_parse(client_reqs):拿到最新数据并存储在数据库中
    get_data()：对外提供数据库最新数据'''
con = database_configure()[2]
# 创建游标对象
cursor = con.cursor()
def data_parse(client_reqs):
    '''存放解析后的数据'''
    '''更新的数据存放在数据库中'''
    humiture15_data = []
    humiture16_data = []
    power79_data = []
    power7A_data = []
    relay_data = []
    for client_req in client_reqs:      #电表可能要发送多条命令,因此采用数组存放指令
        server_resp=connect_server(client_req)                  #连接服务器并响应数据
        '''数据解析'''
        if server_resp[:2]=='15':
            '''温湿度15解析'''
            humidity,temperature=get_humiture(client_req,server_resp)   #得到湿度、温度值
            humiture15_data.append(humidity)
            humiture15_data.append(temperature)
            '''将改动的新数据添加到数据库'''
            cursor.execute('insert into t_humiture15(humi_15,temp_15,time) '
                           'values (%s,%s,NOW())',
                           args=(
                               humiture15_data[0], humiture15_data[1]))
        elif server_resp[:2]=='16':
            '''温湿度16解析'''
            humidity,temperature=get_humiture(client_req,server_resp)   #得到湿度、温度值
            humiture16_data.append(humidity)
            humiture16_data.append(temperature)
            '''将改动的新数据添加到数据库'''
            cursor.execute('insert into t_humiture16(humi_16,temp_16,time) '
                           'values (%s,%s,NOW())',
                           args=(
                               humiture16_data[0], humiture16_data[1]))
        elif server_resp[:2]=='79':
            flag=False
            '''电表解析'''
            if client_req[4:6]=='20':
                battery=get_electric_energy(client_req,server_resp)
                battery=str(f'{battery:.2f}')+'V'#电量
                current,power=get_current_power(client_req,server_resp)
                current=str(f'{current:.2f}')+'A'#电流
                power=str(f'{power*1000:.2f}')+'W'#功率
                power79_data.append(battery)
                power79_data.append(current)
                power79_data.append(power)
            else:
                electric_energy=get_electric_energy(client_req,server_resp)#电能
                electric_energy=str(f'{electric_energy:.2f}')+'kWh'
                power79_data.append(electric_energy)
                flag=True
            '''将改动的新数据添加到数据库'''
            if(flag):
                cursor.execute('insert into t_power79(battery_79,current_79,power_79,electric_energy_79,time) '
                               'values (%s,%s, %s, %s,NOW())',
                               args=(
                                   power79_data[0], power79_data[1], power79_data[2], power79_data[3]))
        elif server_resp[:2]=='7A':
            flag = False
            '''电表解析'''
            if client_req[4:6]=='20':
                battery=get_electric_energy(client_req,server_resp)
                battery=str(f'{battery:.2f}')+'V'#电量
                current,power=get_current_power(client_req,server_resp)
                current=str(f'{current:.2f}')+'A'#电流
                power=str(f'{power*1000:.2f}')+'W'#功率
                power7A_data.append(battery)
                power7A_data.append(current)
                power7A_data.append(power)
            else:
                electric_energy=get_electric_energy(client_req,server_resp)#电能
                electric_energy=str(f'{electric_energy:.2f}')+'kWh'
                power7A_data.append(electric_energy)
                flag = True
            '''将改动的新数据添加到数据库'''
            if (flag):
                cursor.execute('insert into t_power7A(battery_7A,current_7A,power_7A,electric_energy_7A,time) '
                               'values (%s,%s, %s, %s,NOW())',
                               args=(
                                   power7A_data[0], power7A_data[1], power7A_data[2], power7A_data[3]))
        elif client_req[:4]=='0603' : #继电器有关 读 操作

            '''继电器解析'''
            if client_req[4:8]=='0100':     #继电器状态 1-8路
                relay_state=check_relay_state(client_req,server_resp)
                relay_data.append(relay_state)
                '''将改动的新数据添加到数据库'''
                cursor.execute('insert into t_relay(crossing_1,crossing_2,crossing_3,crossing_4,'
                               'crossing_5,crossing_6,crossing_7,crossing_8,time) '
                               'values (%s,%s,%s,%s,%s,%s,%s,%s,NOW())',
                               args=(relay_data[0][7], relay_data[0][6],relay_data[0][5],relay_data[0][4],
                                    relay_data[0][3],relay_data[0][2], relay_data[0][1],relay_data[0][0]))
            if client_req[4:8]=='0101':     #继电器状态 9-16路
                relay_state = check_relay_state(client_req, server_resp)
                relay_data.append(relay_state)
        elif client_req[:4]=='0610':    #继电器有关 写 操作
            down_1_to_8_lst, down_9_to_16_lst, up_1_to_8_lst, up_9_to_16_lst=change_relay_state(client_req,server_resp)#1-16路开关位置
            print(down_1_to_8_lst, down_9_to_16_lst, up_1_to_8_lst, up_9_to_16_lst)

    return humiture15_data,humiture16_data,power79_data,power7A_data,relay_data

'''
data=['22.2%', '22.2℃', '66.6%', '26.6℃', '0', '0', '0', '0', '0', '0', '0', '0', '00000000']
data_var={'15': {'humi': '22.2%', 'temp': '22.2℃'}, '16': {'humi': '66.6%', 'temp': '26.6℃'}}
'''
def get_data():
    data = []

    sensor_list = read_sensor_addr_info()
    sensor_table_name_list=['t_humiture'+i for i in sensor_list]#根据传感器地址得到表名
    data_var={}

    power_list = read_power_addr_info()
    power_table_name_list = ['t_power' + i for i in power_list]  # 根据传感器地址得到表名
    power_data_var = {}


# '''获得传感器温湿度值'''
    for table_name in sensor_table_name_list:
        # 找到表中id最大值
        cursor.execute(f'select max(id) from {table_name} ')
        humiture_max = cursor.fetchone()[0]  # fetchone() 会将查询到的结果放在元组中
        # 查找id最大的这一行
        cursor.execute(f'select * from {table_name} where id=%s', (humiture_max,))
        humi, temp = cursor.fetchone()[1:3]
        data_var[table_name[-2:]] = {'humi':humi,'temp':temp}#{'15': {'humi': '22.2%', 'temp': '22.2℃'}, '16': {'humi': '66.6%', 'temp': '26.6℃'}}
        data.append(humi)
        data.append(temp)

#’‘’获取电表值‘’‘
    for table_name in power_table_name_list:
        # 找到表中id最大值
        cursor.execute(f'select max(id) from {table_name} ')
        power_max = cursor.fetchone()[0]  # fetchone() 会将查询到的结果放在元组中
        # 查找id最大的这一行
        cursor.execute(f'select * from {table_name} where id=%s', (power_max,))
        battery, current, power, electric_energy = cursor.fetchone()[1:5]
        power_data_var[table_name[-2:]] = {'battery': battery, 'current': current,'power': power,'electric_energy': electric_energy}
        data.append(battery)  # 电量
        data.append(current)  # 电流
        data.append(power)  # 功率
        data.append(electric_energy)  # 电能


    '''获得继电器状态'''
    # 找到表中id最大值
    cursor.execute('select max(id) from t_relay ')
    relay_max = cursor.fetchone()[0]  # fetchone() 会将查询到的结果放在元组中
    # 查找id最大的这一行
    cursor.execute('select * from t_relay where id=%s', (relay_max,))
    relay_result = cursor.fetchone()[1:]
    relay_data="".join(relay_result[:-1])
    data.append(relay_data)
    return data,data_var,power_data_var

if __name__ == '__main__':
    '''
    client_reqs = ['150300000002C71F', '160300000002C72C',  # 15温湿度、16温湿度
                   '79032000001045BE','790340000006DA70', # 79电量，79电能
                   '7A0320000010458D','7A0340000006DA43',  # 7A电量，7A电能
                   '0603010000018441']  # 1-8路
    '''
    # humiture15_data,humiture16_data,power79_data,power7A_data,relay_data=data_parse(['160300000002C72C'])

    data,data_var,power_data_var=get_data()
    print(data)
    print(data_var)
    print(power_data_var)
