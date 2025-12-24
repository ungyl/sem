# -*- coding: utf-8 -*-
#创建时间：2025/8/30 10:30
from project.create_table import create_table
from project.esp32_server import esp32_server
from project.data_show_interface import run_timing
import threading

if __name__ == '__main__':
    '''使用线程开启服务器'''
    server_thread =threading.Thread(target=esp32_server)
    server_thread.start()

    '''创建表结构'''
    create_table()
    '''数据显示界面'''
    '''开启定时'''
    run_timing()
