# -*- coding: utf-8 -*-
#创建时间：2025/8/31 15:35
from project.database_configure import database_configure
from project.read_write_info import read_sensor_addr_info, read_power_addr_info


def create_table():
    con=database_configure()[2]

    #创建游标对象
    cursor=con.cursor()
    '''创建表'''
#传感器
    sensor_var={}#{'15':{建表，初始化}，‘16’：{建表，初始化},。。。}
    sensor_list=read_sensor_addr_info()#['15','16',...]
    sensor_table_name_list = ['t_humiture' + i for i in sensor_list]  # 根据传感器地址得到表名
    for table_name in sensor_table_name_list:
        humi='humi_'+table_name[-2:]
        temp='temp_'+table_name[-2:]
        sensor_sql=f'''
            create table if not exists {table_name}(
            id int primary key auto_increment,
            {humi} varchar(10) default 0,
            {temp} varchar(10) default 0,
            time datetime
            ) engine=InnoDB default charset=utf8;
        '''
        sensor_init_sql=f'''
        INSERT INTO {table_name} ({humi}, {temp}, `time`)
        SELECT '0','0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);
        '''
        sensor_var[table_name[-2:]]= {'sensor_sql':sensor_sql,'sensor_init_sql':sensor_init_sql}
#智能电表
    power_var = {}  # {'79':{建表，初始化}，‘7A’：{建表，初始化},。。。}
    power_list = read_power_addr_info()  # ['79','7A',...]
    power_table_name_list = ['t_power' + i for i in power_list]  # 根据传感器地址得到表名
    for table_name in power_table_name_list:
        battery='battery_'+table_name[-2:]
        current='current_'+table_name[-2:]
        power='power_'+table_name[-2:]
        electric_energy='electric_energy_'+table_name[-2:]
        power_sql=f'''
            create table if not exists {table_name}(
            id int primary key auto_increment,
            {battery} varchar(10) default 0,
            {current} varchar(10) default 0,
            {power} varchar(10) default 0,
            {electric_energy} varchar(10) default 0,
            time datetime
            ) engine=InnoDB default charset=utf8;
        '''
        power_init_sql=f'''
            INSERT INTO {table_name} ({battery}, {current}, {power}, {electric_energy}, `time`)
            SELECT '0','0','0','0', NOW()
            WHERE NOT EXISTS (SELECT 1 FROM {table_name} LIMIT 1);
        '''
        power_var[table_name[-2:]]= {'power_sql':power_sql,'power_init_sql':power_init_sql}

    '''创建继电器表'''
    relay_sql = '''
        create table if not exists t_relay(
        id int primary key auto_increment,
        crossing_1 char(1),
        crossing_2 char(1),
        crossing_3 char(1),
        crossing_4 char(1),
        crossing_5 char(1),
        crossing_6 char(1),
        crossing_7 char(1),
        crossing_8 char(1),
        time datetime
        ) engine=InnoDB default charset=utf8;
            '''
    relay_init_sql='''
        INSERT INTO t_relay (crossing_1, crossing_2, crossing_3, crossing_4,
                     crossing_5, crossing_6, crossing_7, crossing_8, `time`)
        SELECT '0','0','0','0','0','0','0','0', NOW()
        WHERE NOT EXISTS (SELECT 1 FROM t_relay LIMIT 1);
    '''

    #使用游标对象，执行sql
    for sensor_addr in sensor_list:
        cursor.execute(sensor_var[sensor_addr]['sensor_sql'])
        cursor.execute(sensor_var[sensor_addr]['sensor_init_sql'])

    for power_addr in power_list:
        cursor.execute(power_var[power_addr]['power_sql'])
        cursor.execute(power_var[power_addr]['power_init_sql'])

    cursor.execute(relay_sql)
    cursor.execute(relay_init_sql)

    con.close()


if __name__ == '__main__':
    data = ['34.3%', '23.4℃', '34.3%', '23.4℃',
            '0.07', '0.15','0.07', '0.15',
            '0.07', '0.15', '0.07', '0.15',
            '关开开关关开关关']
    create_table()