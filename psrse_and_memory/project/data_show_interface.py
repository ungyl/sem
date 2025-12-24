# -*- coding: utf-8 -*-
# 创建时间：2025/9/3 8:19
import os
import re
from tkinter import *
from tkinter import messagebox

from project.create_table import create_table
from project.database_configure import database_configure
from project.get_data import get_data, data_parse
import sched
import time
import threading
from datetime import datetime, timedelta
from project.insert_user_information import insert_user_data
from project.read_write_info import *
from project.read_write_info import change_into_command

'''
    Application(Frame)  创建数据界面的类
    1.register_interface(login_root)    注册
    2.login_interface() 登录
    3.back_to_login() 数据界面返回登录界面
    4.timing_setxx  节点定时设置
'''

con = database_configure()[2]
# 创建游标对象
cursor = con.cursor()
role_var = None
class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        # 存储每个地址的变量（避免循环覆盖）
        self.sensor_vars = {}
        self.power_vars={}

        self.last_sensor_list=[]
        self.last_power_list=[]
        self.humiture_show=None
        self.power_show=None

        # 只建一次控件
        self.createWidget()

        self.start_device_monitor()

        #控制不同角色的界面显示
        self.setting_on_or_down()

        # 定时器变量
        self.after_id = None
        self.set_freq(60)  # 默认 5次/分

#'''渲染界面2'''
    def setting(self):  # 设置操作
        setting_root = Toplevel(self)
        setting_root.title('设置')
        setting_root.geometry('550x300+200+300')

        #传感器
        sensor_addr_list=read_sensor_addr_info()
        for row, addr in enumerate(sensor_addr_list):
            Label(setting_root, text=f"{addr}  ").grid(row=row, column=0)
            Label(setting_root, text="定时状态: ").grid(row=row, column=1)
            # 动态创建 BooleanVar 并设置默认值
            switch_var_name = f"switch_var_{addr}"
            switch_var = BooleanVar()
            setattr(self, switch_var_name, switch_var)  # self.switch_var_name=switch_var
            # 3. 调用 read_info_15 / read_info_16
            read_func = globals().get("read_sensor_timing")  # 如果 read_info_xx 是全局函数
            # 或者如果你在类里定义了这些方法，用 getattr(self, f"read_info_{addr}", lambda: '')
            info = read_func()[addr] if read_func else ''
            if info != '':switch_var.set(True)
            # 4. 绑定 switch_15 / switch_16 回调
            switch = Checkbutton(
                setting_root,
                variable=switch_var,
                command=lambda a=addr: self.switch_addr(a)  # ← 关键：a=addr 捕获当前值
            )

            switch.grid(row=row, column=2)
            # 5. 创建并保存 Entry 控件（使用 setattr 存到 self）
            Label(setting_root, text="周 ").grid(row=row, column=3)
            entry_workday = Entry(setting_root, width=10)
            setattr(self, f"entry_workday_{addr}", entry_workday)
            entry_workday.grid(row=row, column=4)
            Label(setting_root, text=" ").grid(row=row, column=5)
            entry_begin_hour = Entry(setting_root, width=3)
            setattr(self, f"entry_begin_hour_{addr}", entry_begin_hour)
            entry_begin_hour.grid(row=row, column=6)
            Label(setting_root, text="时").grid(row=row, column=7)
            entry_begin_minute = Entry(setting_root, width=3)
            setattr(self, f"entry_begin_minute_{addr}", entry_begin_minute)
            entry_begin_minute.grid(row=row, column=8)
            Label(setting_root, text="分").grid(row=row, column=9)
            Label(setting_root, text="  ").grid(row=row, column=10)
            entry_end_hour = Entry(setting_root, width=3)
            setattr(self, f"entry_end_hour_{addr}", entry_end_hour)
            entry_end_hour.grid(row=row, column=11)
            Label(setting_root, text="时").grid(row=row, column=12)
            entry_end_minute = Entry(setting_root, width=3)
            setattr(self, f"entry_end_minute_{addr}", entry_end_minute)
            entry_end_minute.grid(row=row, column=13)
            Label(setting_root, text="分").grid(row=row, column=14)
            Label(setting_root, text="  ").grid(row=row, column=15)
            Label(setting_root, text="间隔").grid(row=row, column=16)
            entry_interval = Entry(setting_root, width=4)
            setattr(self, f"entry_interval_{addr}", entry_interval)
            entry_interval.grid(row=row, column=17)
            Label(setting_root, text="  ").grid(row=row, column=18)
            # 6. 绑定 submit_15 / submit_16
            Button(
                setting_root,
                text="确定",
                command=lambda a=addr: self.submit_addr(a)
            ).grid(row=row, column=19)


            #电表
            sensor_row_count=len(sensor_addr_list)
            power_addr_list = read_power_addr_info()
            for row, addr in enumerate(power_addr_list,sensor_row_count):
                Label(setting_root, text=f"{addr}  ").grid(row=row, column=0)
                Label(setting_root, text="定时状态: ").grid(row=row, column=1)
                switch_var_name = f"switch_var_{addr}"
                switch_var = BooleanVar()
                setattr(self, switch_var_name, switch_var)  # self.switch_var_name=switch_var
                read_func = globals().get("read_power_timing")  # 如果 read_info_xx 是全局函数
                info = read_func()[addr] if read_func else ''
                if info != '': switch_var.set(True)
                switch = Checkbutton(
                    setting_root,
                    variable=switch_var,
                    command=lambda a=addr: self.switch_addr(a)
                )
                switch.grid(row=row, column=2)
                Label(setting_root, text="周 ").grid(row=row, column=3)
                entry_workday = Entry(setting_root, width=10)
                setattr(self, f"entry_workday_{addr}", entry_workday)
                entry_workday.grid(row=row, column=4)
                Label(setting_root, text=" ").grid(row=row, column=5)
                entry_begin_hour = Entry(setting_root, width=3)
                setattr(self, f"entry_begin_hour_{addr}", entry_begin_hour)
                entry_begin_hour.grid(row=row, column=6)
                Label(setting_root, text="时").grid(row=row, column=7)
                entry_begin_minute = Entry(setting_root, width=3)
                setattr(self, f"entry_begin_minute_{addr}", entry_begin_minute)
                entry_begin_minute.grid(row=row, column=8)
                Label(setting_root, text="分").grid(row=row, column=9)
                Label(setting_root, text="  ").grid(row=row, column=10)
                entry_end_hour = Entry(setting_root, width=3)
                setattr(self, f"entry_end_hour_{addr}", entry_end_hour)
                entry_end_hour.grid(row=row, column=11)
                Label(setting_root, text="时").grid(row=row, column=12)
                entry_end_minute = Entry(setting_root, width=3)
                setattr(self, f"entry_end_minute_{addr}", entry_end_minute)
                entry_end_minute.grid(row=row, column=13)
                Label(setting_root, text="分").grid(row=row, column=14)
                Label(setting_root, text="  ").grid(row=row, column=15)
                Label(setting_root, text="间隔").grid(row=row, column=16)
                entry_interval = Entry(setting_root, width=4)
                setattr(self, f"entry_interval_{addr}", entry_interval)
                entry_interval.grid(row=row, column=17)
                Label(setting_root, text="  ").grid(row=row, column=18)
                Button(setting_root,
                       text="确定",
                       command=lambda a=addr: self.submit_addr(a)
                       ).grid(row=row, column=19)

            power_row_count=len(power_addr_list)
# 06定时状态
        other_row_count=sensor_row_count+power_row_count
        Label(setting_root, text="06  ").grid(row=other_row_count, column=0)
        Label(setting_root, text="定时状态: ").grid(row=other_row_count, column=1)
        self.switch_var_06 = BooleanVar()
        info_06 = read_info_06()
        if info_06 != '': self.switch_var_06.set(True)  # 文件中有数据时，默认打开
        switch = Checkbutton(setting_root, variable=self.switch_var_06, command=self.switch_06)
        switch.grid(row=other_row_count, column=2)
        Label(setting_root, text="周 ").grid(row=other_row_count, column=3)
        self.entry_workday_06 = Entry(setting_root, width=10)
        self.entry_workday_06.grid(row=other_row_count, column=4)
        Label(setting_root, text=" ").grid(row=other_row_count, column=5)
        self.entry_begin_hour_06 = Entry(setting_root, width=3)
        self.entry_begin_hour_06.grid(row=other_row_count, column=6)
        Label(setting_root, text="时").grid(row=other_row_count, column=7)
        self.entry_begin_minute_06 = Entry(setting_root, width=3)
        self.entry_begin_minute_06.grid(row=other_row_count, column=8)
        Label(setting_root, text="分").grid(row=other_row_count, column=9)
        Label(setting_root, text="  ").grid(row=other_row_count, column=10)
        self.entry_end_hour_06 = Entry(setting_root, width=3)
        self.entry_end_hour_06.grid(row=other_row_count, column=11)
        Label(setting_root, text="时").grid(row=other_row_count, column=12)
        self.entry_end_minute_06 = Entry(setting_root, width=3)
        self.entry_end_minute_06.grid(row=other_row_count, column=13)
        Label(setting_root, text="分").grid(row=other_row_count, column=14)
        Label(setting_root, text="  ").grid(row=other_row_count, column=15)
        Label(setting_root, text="间隔").grid(row=other_row_count, column=16)
        self.entry_interval_06 = Entry(setting_root, width=4)
        self.entry_interval_06.grid(row=other_row_count, column=17)
        Label(setting_root, text="  ").grid(row=other_row_count, column=18)
        Button(setting_root, text="确定", command=self.submit_06).grid(row=other_row_count, column=19)

        # 管理用户
        Button(setting_root, text="管理用户", command=self.set_user).grid(row=other_row_count+1, column=17, columnspan=19)

        # 添加/删除节点
        set_node=Frame(setting_root)
        set_node.grid(row=other_row_count+2, column=0,columnspan=25)
        Button(set_node, text="温湿度传感器", command=lambda:self.set_sensor(other_row_count)).grid(row=other_row_count+2, column=0)
        self.sensor_label=Label(set_node,text=' 地址码 ')
        self.sensor_entry=Entry(set_node,width=5)
        self.add_sensor=Button(set_node,text='确定添加',command=self.add_sensor)
        self.delete_sensor = Button(set_node, text='确定删除',command=self.delete_sensor)
        Button(set_node, text="智能电表", command=lambda:self.set_power(other_row_count)).grid(row=other_row_count+3, column=0)
        self.power_label = Label(set_node, text=' 地址码 ')
        self.power_entry = Entry(set_node, width=5)
        self.add_power = Button(set_node, text='确定添加',command=self.add_power)
        self.delete_power = Button(set_node, text='确定删除',command=self.delete_power)

#添加/删除温湿度传感器
    def set_sensor(self,other_row_count):
        if self.sensor_entry.winfo_ismapped():
            self.sensor_label.grid_remove()
            self.sensor_entry.grid_remove()
            self.add_sensor.grid_remove()
            self.delete_sensor.grid_remove()
        else:  # 隐藏→显示
            self.sensor_label.grid(row=other_row_count+2,column=1)
            self.sensor_entry.grid(row=other_row_count+2, column=2, padx=(0, 5))
            self.add_sensor.grid(row=other_row_count+2, column=3)
            self.delete_sensor.grid(row=other_row_count+2, column=4)
    def add_sensor(self):
        sensor_addr=self.sensor_entry.get()
        if len(sensor_addr)!=2:
            messagebox.showinfo('提示','地址码只能2位')
            return
        sensor_list = read_sensor_addr_info()
        #判断地址码是否在sensor_list中，如果存在，提示：设备已存在；否则，添加设备
        if sensor_addr not in sensor_list:
            # 生成info_addr.txt,方便后续写入定时命令
            open(f'../info_timing/info_{sensor_addr}.txt', 'w').close()
            # 追加
            with open('../info_addr/sensor_addr_info.txt', 'a') as f:
                f.write(sensor_addr)
            create_table()#设备添加成功后，创建表
        else:messagebox.showinfo('提示','设备已存在')

    def delete_sensor(self):
        sensor_addr = self.sensor_entry.get()
        if len(sensor_addr) != 2:
            messagebox.showinfo('提示', '地址码只能2位')
            return
        with open('../info_addr/sensor_addr_info.txt', 'r') as f:
            s=f.read()
            sensor_list = [s[i:i + 2] for i in range(0, len(s), 2)] #传感器地址所组成的列表
        # 判断地址码是否在sensor_list中，如果存在，提示：设备已删除；否则，没有该设备
        if sensor_addr in sensor_list:
            # 删除info_addr.txt
            if os.path.exists(f'../info_timing/info_{sensor_addr}.txt'):
                os.remove(f'../info_timing/info_{sensor_addr}.txt')
            # 覆盖
            with open('../info_addr/sensor_addr_info.txt', 'w') as f:
                f.write(s.replace(sensor_addr,''))
        else:messagebox.showinfo('提示', '没有该设备')


    #添加/删除智能电表
    def set_power(self,other_row_count):
        if self.power_entry.winfo_ismapped():
            self.power_label.grid_remove()
            self.power_entry.grid_remove()
            self.add_power.grid_remove()
            self.delete_power.grid_remove()
        else:  # 隐藏→显示
            self.power_label.grid(row=other_row_count+3, column=1)
            self.power_entry.grid(row=other_row_count+3, column=2, padx=(0, 5))
            self.add_power.grid(row=other_row_count+3, column=3)
            self.delete_power.grid(row=other_row_count+3, column=4)
    def add_power(self):
        power_addr = self.power_entry.get()
        if len(power_addr) != 2:
            messagebox.showinfo('提示', '地址码只能2位')
            return
        power_list = read_power_addr_info()
        # 判断地址码是否在power_list中，如果存在，提示：设备已存在；否则，添加设备
        if power_addr not in power_list:
            # 生成info_addr.txt,方便后续写入定时命令
            open(f'../info_timing/info_{power_addr}.txt', 'w').close()
            # 追加
            with open('../info_addr/power_addr_info.txt', 'a') as f:
                f.write(power_addr)
            create_table()  # 设备添加成功后，创建表
        else:messagebox.showinfo('提示', '设备已存在')
    def delete_power(self):
        power_addr = self.power_entry.get()
        if len(power_addr) != 2:
            messagebox.showinfo('提示', '地址码只能2位')
            return
        with open('../info_addr/power_addr_info.txt', 'r') as f:
            s = f.read()
            power_list = [s[i:i + 2] for i in range(0, len(s), 2)]  # 电表地址所组成的列表
        # 判断地址码是否在power_list中，如果存在，提示：设备已删除；否则，没有该设备
        if power_addr in power_list:
            # 删除info_addr.txt
            if os.path.exists(f'../info_timing/info_{power_addr}.txt'):
                os.remove(f'../info_timing/info_{power_addr}.txt')
                # 覆盖
            with open('../info_addr/power_addr_info.txt', 'w') as f:
                f.write(s.replace(power_addr, ''))
        else:messagebox.showinfo('提示', '没有该设备')

    '''
    界面3
    '''

    # 管理员对用户信息操作页面
    def set_user(self):
        user_root = Toplevel(self)
        user_root.geometry('400x400+200+200')
        user_root.title('用户管理')
        self.show_user_data(user_root)
        user_frame = Frame(user_root)
        user_frame.grid(row=1, column=0)
        # 增加用户信息
        Button(user_frame, text="添加用户", command=self.add_user).grid(row=1, column=0)
        self.add_username_label = Label(user_frame, text=' 用户名 ')
        self.add_username_entry = Entry(user_frame, width=10)
        self.add_pwd_label = Label(user_frame, text='  密码 ')
        self.add_pwd_entry = Entry(user_frame, width=10)
        self.add_button = Button(user_frame, text="确定添加", command=self.add_submit)
        # 删除用户信息
        Button(user_frame, text="删除用户", command=self.delet_user).grid(row=2, column=0)
        self.seq_delet_label = Label(user_frame, text=" 序号 ")
        self.delet_entry = Entry(user_frame, width=10)
        self.delet_button = Button(user_frame, text="确定删除", command=self.delet_submit)
        # 修改用户信息
        Button(user_frame, text="修改用户", command=self.update_user).grid(row=3, column=0)
        self.seq_update_label = Label(user_frame, text=" 序号 ")
        self.update_entry = Entry(user_frame, width=10)
        self.update_username_label = Label(user_frame, text=' 用户名 ')
        self.update_username_entry = Entry(user_frame, width=10)
        self.update_pwd_label = Label(user_frame, text='  密码 ')
        self.update_pwd_entry = Entry(user_frame, width=10)
        self.update_button = Button(user_frame, text="确定修改", command=self.update_submit)

    def show_user_data(self,user_root):
        # 创建控件
        self.text = Text(user_root, height=10, width=34, font=("Arial", 14), wrap="none")
        scrollbar1 = Scrollbar(user_root, orient='vertical', command=self.text.yview)
        # 文本占 0 列，滚动条占 1 列
        self.text.grid(row=0, column=0, sticky='nsew')
        scrollbar1.grid(row=0, column=1, sticky='ns')
        # 关联滚动条
        self.text['yscrollcommand'] = scrollbar1.set
        self.fill_user_data()
    def fill_user_data(self):
        self.text.delete('1.0', END)
        cursor.execute('select * from t_user_data')
        user_infos = cursor.fetchall()
        i = 2
        self.text.insert(f'1.0', f'序号\t用户名\t\t密码\n')
        for user_info in user_infos:
            username = user_info[0]
            pwd = user_info[1]
            self.text.insert(f'{i}.0', f'{i - 1}\t{username}\t\t{pwd}\n')
            i += 1
    # 增加用户
    def add_user(self):
        if self.add_username_entry.winfo_ismapped():
            self.add_username_label.grid_remove()
            self.add_username_entry.grid_remove()
            self.add_pwd_label.grid_remove()
            self.add_pwd_entry.grid_remove()
            self.add_button.grid_remove()
        else:  # 隐藏→显示
            self.add_username_label.grid(row=1, column=1)
            self.add_username_entry.grid(row=1, column=2)
            self.add_pwd_label.grid(row=1, column=3)
            self.add_pwd_entry.grid(row=1, column=4, padx=(0, 5))
            self.add_button.grid(row=1, column=5)

    def add_submit(self):
        new_username=self.add_username_entry.get()
        new_pwd=self.add_pwd_entry.get()
        insert_user_data(new_username,new_pwd,'user')
        self.fill_user_data()

    # 删除用户
    def delet_user(self):
        if self.delet_entry.winfo_ismapped():
            self.seq_delet_label.grid_remove()
            self.delet_entry.grid_remove()
            self.delet_button.grid_remove()
        else:  # 隐藏→显示
            self.seq_delet_label.grid(row=2, column=1)
            self.delet_entry.grid(row=2, column=2, padx=(0, 5))
            self.delet_button.grid(row=2, column=3)

    def delet_submit(self):
        delet_seq = self.delet_entry.get()
        cursor.execute('select count(*) from t_user_data')
        user_num = cursor.fetchone()[0]  # 用户数量
        if delet_seq!='' and (int(delet_seq)>=1 and int(delet_seq)<=user_num):
            delet_seq = int(self.delet_entry.get())
            cursor.execute('select * from t_user_data limit %s,1',args=(delet_seq-1,))
            delet_username=cursor.fetchone()[0]
            cursor.execute('delete from t_user_data where username=%s',args=(delet_username,))
            self.fill_user_data()
        else:messagebox.showinfo("提示","请输入要删除用户信息的序号")

    # 修改用户
    def update_user(self):
        if self.update_entry.winfo_ismapped():
            self.seq_update_label.grid_remove()
            self.update_entry.grid_remove()
            self.update_button.grid_remove()
            self.update_username_label.grid_remove()
            self.update_username_entry.grid_remove()
            self.update_pwd_label.grid_remove()
            self.update_pwd_entry.grid_remove()
            self.update_button.grid_remove()

        else:  # 隐藏→显示
            self.seq_update_label.grid(row=3, column=1)
            self.update_entry.grid(row=3, column=2, padx=(0, 5))
            self.update_button.grid(row=3, column=3)
            self.update_username_label.grid(row=4, column=1)
            self.update_username_entry.grid(row=4, column=2)
            self.update_pwd_label.grid(row=4, column=3)
            self.update_pwd_entry.grid(row=4, column=4, padx=(0, 5))
            self.update_button.grid(row=4, column=5)

    def update_submit(self):
        update_seq = self.update_entry.get()
        cursor.execute('select count(*) from t_user_data')
        user_num = cursor.fetchone()[0]  # 用户数量
        if update_seq != '' and (int(update_seq)>=1 and int(update_seq)<=user_num):
            update_seq = int(self.update_entry.get())
            cursor.execute('select * from t_user_data limit %s,1', args=(update_seq - 1,))
            update_username,update_pwd= cursor.fetchone()#要修改的用户信息
            new_username=self.update_username_entry.get()
            new_pwd=self.update_pwd_entry.get()
            if new_username=='':new_username=update_username
            if new_pwd=='':new_pwd=update_pwd

            try:
                cursor.execute('update t_user_data set username=%s,pwd=%s where username=%s',args=(new_username,new_pwd,update_username))
            except:
                messagebox.showinfo("提示","用户名已存在，修改失败")
            self.fill_user_data()
        else:messagebox.showinfo("提示","请输入要修改用户信息的序号")
    '''
    定时设置
    '''

    # ==================== 通用提交函数 ====================
    def submit_addr(self, addr):
        '''通用提交函数，addr 为整数（如 15, 16, 22）'''
        # 动态获取 Entry 值
        try:
            workday = getattr(self, f"entry_workday_{addr}").get()
            begin_hour = getattr(self, f"entry_begin_hour_{addr}").get()
            begin_minute = getattr(self, f"entry_begin_minute_{addr}").get()
            end_hour = getattr(self, f"entry_end_hour_{addr}").get()
            end_minute = getattr(self, f"entry_end_minute_{addr}").get()
            interval = getattr(self, f"entry_interval_{addr}").get()
        except AttributeError:
            messagebox.showerror("错误", f"未找到地址 {addr} 的输入控件")
            return

        # 验证逻辑（和你原来完全一致）
        if workday == '' or re.match(r'^[1-7]{1,7}$', workday) is None:
            flag = False
        elif begin_hour == '' or re.match(r'^\d|1\d|2[0-3]$', begin_hour) is None:
            flag = False
        elif begin_minute == '' or re.match(r'^\d|[1-5]\d$', begin_minute) is None:
            flag = False
        elif end_hour == '' or re.match(r'^\d|1\d|2[0-3]$', end_hour) is None:
            flag = False
        elif end_minute == '' or re.match(r'^\d|[1-5]\d$', end_minute) is None:
            flag = False
        elif interval == '' or re.match(r'^\d|[1-9]\d|1[01]\d|120$', interval) is None:
            flag = False
        else:
            flag = True

        if not flag:
            messagebox.showinfo('提示', '设置失败')
            return

        # 构造命令（保持和你原来一致：DDEEFF15...）
        command = f"DDEEFF{addr}" + change_into_command(
            workday, begin_hour, begin_minute, end_hour, end_minute, interval
        )

        write_func_name = f"write_info"
        if write_func_name in globals() and callable(globals()[write_func_name]):
            globals()[write_func_name](addr,command)

        else:
            messagebox.showerror("错误", f"未找到函数 {write_func_name}")
            return
        messagebox.showinfo('提示', '设置成功')

    # ==================== 通用开关函数 ====================
    def switch_addr(self, addr):
        '''通用开关函数，addr 为整数'''
        switch_var = getattr(self, f"switch_var_{addr}", None)
        if switch_var is None:
            return

        if not switch_var.get():
            # 清空对应文件（和你原来一致）
            filepath = f'../info_timing/info_{addr}.txt'
            open(filepath, 'w').close()


    # 06的定时设置
    def submit_06(self):
        '''将接受到的数据还原成原始数据'''
        flag_06 = True
        workday_06 = self.entry_workday_06.get()
        begin_hour_06 = self.entry_begin_hour_06.get()
        begin_minute_06 = self.entry_begin_minute_06.get()
        end_hour_06 = self.entry_end_hour_06.get()
        end_minute_06 = self.entry_end_minute_06.get()
        interval_06 = self.entry_interval_06.get()

        if (workday_06 == '' or re.match(r'^[1-7]{1,7}$', workday_06) == None):
            flag_06 = False
        elif (begin_hour_06 == '' or re.match(r'^\d|1\d|2[0-3]$', begin_hour_06) == None):
            flag_06 = False
        elif (begin_minute_06 == '' or re.match(r'^\d|[1-5]\d$', begin_minute_06) == None):
            flag_06 = False
        elif (end_hour_06 == '' or re.match(r'^\d|1\d|2[0-3]$', end_hour_06) == None):
            flag_06 = False
        elif (end_minute_06 == '' or re.match(r'^\d|[1-5]\d$', end_minute_06) == None):
            flag_06 = False
        elif (interval_06 == '' or re.match(r'^\d|[1-9]\d|1[01]\d|120$', interval_06) == None):
            flag_06 = False

        if flag_06 == False:
            messagebox.showinfo('提示', '设置失败')
        if flag_06 == True:
            command = "DDEEFF06" + change_into_command(workday_06, begin_hour_06, begin_minute_06, end_hour_06,
                                                       end_minute_06, interval_06)
            write_info_06(command)
            messagebox.showinfo('提示', '设置成功')

    def switch_06(self):
        if self.switch_var_06.get():
            pass
        else:
            open('../info_timing/info_06.txt', 'w').close()  # 取消勾选框，定时取消，文本数据清除

    #setting按键的显示与否
    def setting_on_or_down(self):
        '''user：setting在登录后就销毁
            admin:setting在登录后就创建'''
        if role_var.get()=='user':
            self.btn_setting.grid_remove()
        elif role_var.get()=='admin':
            self.btn_setting.grid(row=0, column=20)

    # 1️只建一次控件
    def createWidget(self):
        # 标题
        Button(self,text='←',command=back_to_login).grid(row=0, column=0,sticky='W')
        Label(self, text='数据显示系统', height=2,font=("微软雅黑", 12, "bold")).grid(row=0, column=0, columnspan=25)
        self.btn_setting=Button(self, text='setting', command=self.setting)
        '''传感器'''
        sensor_list = read_sensor_addr_info()
        row = 2
        if len(sensor_list)!=0:
            self.humiture_show=Frame(self)
            self.humiture_show.grid(row=row, column=0)
            Label(self.humiture_show, text='1.温湿度数据',font=("微软雅黑", 8, "bold")).grid(row=1, column=0)
            for addr in sensor_list:
                Label(self.humiture_show, text=f'地址  {addr} ').grid(row=row, column=0)
                self.humi_var, self.temp_var = StringVar(), StringVar()     #湿度、温度
                self.timing_data_var = StringVar()
                self.sensor_vars[addr] = {'humi': self.humi_var, 'temp': self.temp_var,'timing':self.timing_data_var}
                Label(self.humiture_show, text='湿度').grid(row=row, column=11)
                Label(self.humiture_show, width=5, height=1, textvariable=self.humi_var).grid(row=row, column=13)
                Label(self.humiture_show, text='温度').grid(row=row, column=21)
                Label(self.humiture_show, width=5, height=1, textvariable=self.temp_var).grid(row=row, column=23)
                row+=1
                Label(self.humiture_show, text="定时信息：").grid(row=row, column=0)
                Label(self.humiture_show, height=1, textvariable=self.timing_data_var).grid(row=row, column=11, columnspan=25)
                row+=1
        '''智能电表'''
        power_list = read_power_addr_info()
        if len(power_list) != 0:
            self.power_show = Frame(self)
            self.power_show.grid(row=row, column=0)
            Label(self.power_show, text='2.电量电能数据', font=("微软雅黑", 8, "bold")).grid(row=row, column=0)
            row+=1
            for addr in power_list:
                Label(self.power_show, text=f'地址  {addr} ').grid(row=row, column=0)
                self.battery = StringVar()
                self.energy = StringVar()
                self.current = StringVar()
                self.power = StringVar()
                self.timing_data = StringVar()
                self.power_vars[addr] = {'battery': self.battery, 'electric_energy': self.energy,'current':self.current,'power':self.power,'timing':self.timing_data}
                Label(self.power_show, text='电量').grid(row=row, column=11)
                Label(self.power_show, width=7, height=1, textvariable=self.battery).grid(row=row, column=13)
                Label(self.power_show, text='电能').grid(row=row, column=21)
                Label(self.power_show, width=7, height=1, textvariable=self.energy).grid(row=row, column=23)
                row+=1
                Label(self.power_show, text='电流').grid(row=row, column=11)
                Label(self.power_show, width=7, height=1, textvariable=self.current).grid(row=row, column=13)
                Label(self.power_show, text='功率').grid(row=row, column=21)
                Label(self.power_show, width=7, height=1, textvariable=self.power).grid(row=row, column=23)
                row+=1
                Label(self.power_show, text="定时信息：").grid(row=row, column=0)
                Label(self.power_show, height=1, textvariable=self.timing_data).grid(row=row, column=11, columnspan=25)
                row+=1

        # 继电器
        self.frame_relay = Frame(self)
        self.frame_relay.grid(row=15, column=0)
        Label(self.frame_relay, text='3.继电器各路状态',font=("微软雅黑", 8, "bold")).grid(row=13, column=0)
        self.relay_lbls = []
        for i in range(8):
            Label(self.frame_relay, text=i + 1).grid(row=15, column=3 * i)
            lbl = Label(self.frame_relay, text='?')
            lbl.grid(row=16, column=3 * i)
        relay_timing = Frame(self.frame_relay)
        relay_timing.grid(row=17, column=0, columnspan=25, sticky='E')
        Label(relay_timing, text="定时信息：").grid(row=17, column=0, padx=(0, 20))
        self.timing_data_06 = StringVar()
        Label(relay_timing, height=1, textvariable=self.timing_data_06).grid(row=17, column=11)

        # 控制区 + Scale（只建一次）
        control = Frame(self)
        control.grid(row=18, column=0, columnspan=50)
        Label(control, text='自动刷新频次').grid(row=18, column=0)
        self.freq = Label(control, width=5, text='5')
        self.freq.grid(row=18, column=16)
        Label(control, text='次/分').grid(row=18, column=21)
        Button(control, text='刷新', command=self.refresh).grid(row=18, column=35, padx=(40, 50))
        self.scale = Scale(self, from_=5, to=20, length=100, tickinterval=5,
                           orient=HORIZONTAL, command=self.set_freq)
        self.scale.grid(row=19, column=0)


    # 检测设备变化并重建传感器/电表界面
    def check_device_change(self):
        # 获取最新设备列表
        current_sensor = read_sensor_addr_info()
        current_power = read_power_addr_info()

        # 检测是否变化（排序后对比，避免顺序影响）
        sensor_changed = sorted(current_sensor) != sorted(self.last_sensor_list)
        power_changed = sorted(current_power) != sorted(self.last_power_list)

        if sensor_changed or power_changed:
            # 1. 删除旧的传感器Frame（如果存在）
            if self.humiture_show:
                self.humiture_show.destroy()
                self.humiture_show = None
            # 2. 删除旧的电表Frame（如果存在）
            if self.power_show:
                self.power_show.destroy()
                self.power_show = None

            # 3. 重置变量（避免旧数据干扰）
            self.sensor_vars = {}
            self.power_vars = {}

            # 4. 更新历史列表
            self.last_sensor_list = current_sensor.copy()
            self.last_power_list = current_power.copy()

            # 5. 重新创建传感器/电表部分
            self.rebuild_sensor_power()

    # 【新增】单独重建传感器/电表界面（完全复用你的原有逻辑）
    def rebuild_sensor_power(self):
        '''传感器'''
        sensor_list = read_sensor_addr_info()
        row = 2
        if len(sensor_list) != 0:
            self.humiture_show = Frame(self)
            self.humiture_show.grid(row=row, column=0)
            Label(self.humiture_show, text='1.温湿度数据', font=("微软雅黑", 8, "bold")).grid(row=1, column=0)
            for addr in sensor_list:
                Label(self.humiture_show, text=f'地址  {addr} ').grid(row=row, column=0)
                self.humi_var, self.temp_var = StringVar(), StringVar()
                self.timing_data_var = StringVar()
                self.sensor_vars[addr] = {'humi': self.humi_var, 'temp': self.temp_var, 'timing': self.timing_data_var}
                Label(self.humiture_show, text='湿度').grid(row=row, column=11)
                Label(self.humiture_show, width=5, height=1, textvariable=self.humi_var).grid(row=row, column=13)
                Label(self.humiture_show, text='温度').grid(row=row, column=21)
                Label(self.humiture_show, width=5, height=1, textvariable=self.temp_var).grid(row=row, column=23)
                row += 1
                Label(self.humiture_show, text="定时信息：").grid(row=row, column=0)
                Label(self.humiture_show, height=1, textvariable=self.timing_data_var).grid(row=row, column=11,
                                                                                            columnspan=25)
                row += 1
        '''智能电表'''
        power_list = read_power_addr_info()
        if len(power_list) != 0:
            self.power_show = Frame(self)
            self.power_show.grid(row=row, column=0)
            Label(self.power_show, text='2.电量电能数据', font=("微软雅黑", 8, "bold")).grid(row=row, column=0)
            row += 1
            for addr in power_list:
                Label(self.power_show, text=f'地址  {addr} ').grid(row=row, column=0)
                self.battery = StringVar()
                self.energy = StringVar()
                self.current = StringVar()
                self.power = StringVar()
                self.timing_data = StringVar()
                self.power_vars[addr] = {'battery': self.battery, 'electric_energy': self.energy,
                                         'current': self.current, 'power': self.power, 'timing': self.timing_data}
                Label(self.power_show, text='电量').grid(row=row, column=11)
                Label(self.power_show, width=7, height=1, textvariable=self.battery).grid(row=row, column=13)
                Label(self.power_show, text='电能').grid(row=row, column=21)
                Label(self.power_show, width=7, height=1, textvariable=self.energy).grid(row=row, column=23)
                row += 1
                Label(self.power_show, text='电流').grid(row=row, column=11)
                Label(self.power_show, width=7, height=1, textvariable=self.current).grid(row=row, column=13)
                Label(self.power_show, text='功率').grid(row=row, column=21)
                Label(self.power_show, width=7, height=1, textvariable=self.power).grid(row=row, column=23)
                row += 1
                Label(self.power_show, text="定时信息：").grid(row=row, column=0)
                Label(self.power_show, height=1, textvariable=self.timing_data).grid(row=row, column=11, columnspan=25)
                row += 1

    # 【新增】定时检测（循环执行）
    def start_device_monitor(self, interval=1000):  # interval=1000表示1秒检测一次
        self.check_device_change()
        # 定时调用自己，实现循环检测
        self.after(interval, lambda: self.start_device_monitor(interval))


    '''power_data_dict={'7A': {'battery': '218.30V', 'current': '0.00A', 'power': '0.00W', 
                'electric_energy': '0.37kWh', 'timing': [8, 0, 23, 0, {1, 2, 3, 4, 5, 6, 7}, 120]}, 
                '79': {'battery': '217.90V', 'current': '0.00A', 'power': '0.00W', 
                'electric_energy': '5.21kWh', 'timing': [8, 0, 23, 0, {1, 2, 3, 4, 5, 6, 7}, 120]}}'''
    # 2️只更新数据
    def update_data(self, data):
        sensor_list = read_sensor_addr_info()#传感器地址组成的列表
        data_var = get_data()[1]#拿到存放温湿度数据的字典
        timing_data_var = get_timing_data()[1]
        data_dict = {k: {**data_var[k], 'timing': timing_data_var[k]} for k in data_var}#包含温湿度、定时的数据
        for addr in sensor_list:
            try:
                self.sensor_vars[addr]['humi'].set(data_dict[addr]['humi'])     #根据传感器设备地址，为湿度、温度、定时 分配数据
                self.sensor_vars[addr]['temp'].set(data_dict[addr]['temp'])
                self.sensor_vars[addr]['timing'].set(data_dict[addr]['timing'])
            except:
                pass

        power_list = read_power_addr_info()
        power_data_var = get_data()[2]
        timing_power_data_var = get_timing_data()[2]
        power_data_dict = {k: {**power_data_var[k], 'timing': timing_power_data_var[k]} for k in power_data_var}
        for addr in power_list:
                try:
                    self.power_vars[addr]['battery'].set(power_data_dict[addr]['battery'])  # 根据传感器设备地址，为湿度、温度、定时 分配数据
                    self.power_vars[addr]['electric_energy'].set(power_data_dict[addr]['electric_energy'])
                    self.power_vars[addr]['current'].set(power_data_dict[addr]['current'])
                    self.power_vars[addr]['power'].set(power_data_dict[addr]['power'])
                    self.power_vars[addr]['timing'].set(power_data_dict[addr]['timing'])
                except:
                    pass

        #继电器各路状态
        data_1_8 = data[-1]
        for i in range(8):
            relay_state = data_1_8[i]
            Label(self.frame_relay, text=relay_state).grid(row=16, column=3 * i)

        # 读出数据06定时数据
        info_06 = get_timing_data()[0][-1]
        self.timing_data_06.set(info_06)

    # 3️频率 & 定时
    def set_freq(self, value):
        self.freq['text'] = value
        if self.after_id:
            self.after_cancel(self.after_id)
        if int(value) == 0:  # 0 → 不刷新
            return
        ms = 60 * 1000 // int(value)
        self.after_id = self.after(ms, self.refresh)

    def refresh(self):
        data = get_data()[0]  # 获得最新数据
        self.update_data(data)
        self.set_freq(self.freq['text'])  # 继续下一轮  滑条控制定时

'''注册普通用户界面'''
def register_interface(login_root):
    def add_information():      #将新的账号、密码 ，根据角色状态添加到数据库中
        insert_user_data(new_username.get(),new_pwd.get(),role_var.get())

    def return_login_interface():#返回到登录界面
        register_root.destroy()
        login_interface()

    login_root.destroy()
    register_root=Tk()
    register_root.title('注册界面')
    register_root.geometry('500x300+200+300')
    '''新账号'''
    label_username = Label(register_root,text='新账号：')
    label_username.grid(row=0, column=0, padx=(150, 0), pady=(50, 0))
    new_username = StringVar()
    entry_username = Entry(register_root,textvariable=new_username)
    entry_username.grid(row=0, column=1, columnspan=2, padx=10, pady=(50, 0))
    '''新密码'''
    label_pwd = Label(register_root,text='新密码：')
    label_pwd.grid(row=1, column=0, padx=(150, 0), pady=(10, 0))
    new_pwd = StringVar()
    entry_pwd = Entry(register_root,textvariable=new_pwd)
    entry_pwd.grid(row=1, column=1, columnspan=2, padx=10, pady=(10, 0))
    '''确定'''
    btn_login = Button(register_root,text='确定', command=add_information)
    btn_login.grid(row=2, column=1, pady=(10, 0))
    '''返回'''
    Button(register_root, text='返回', command=return_login_interface).grid(row=2, column=2, pady=(10, 0))
    register_root.mainloop()

'''登录界面'''
show_root=None
login_done_event = threading.Event()
app=None
print(id(app))

def login_interface():

    def click_login():  #比对账号密码，跳转数据显示页面
        print(role_var.get())
        '''user:进入普通用户界面，此时不显示setting按钮'''
        if role_var.get()=='user':
            user_data=database_configure()[1]   #从数据库中拿到用户数据
            dict_user_data=dict(user_data)      #将账号密码转换成字典
            usernames = [index for index in dict_user_data.keys()]
            if username.get() in usernames and dict_user_data[username.get()]==pwd.get():#账号存在，并且输入的密码对应
               create_interface()
            else:messagebox.showinfo('Tip', '账号或密码有误！')
        #'''admin:进入管理员界面，此时显示setting按钮，可以修改部分数据'''
        elif role_var.get()=='admin':
            user_data = database_configure()[3]  # 从数据库中拿到用户数据
            dict_user_data = dict(user_data)  # 将账号密码转换成字典
            usernames = [index for index in dict_user_data.keys()]
            if username.get() in usernames and dict_user_data[username.get()] == pwd.get():  # 账号存在，并且输入的密码对应
                create_interface()
            else:messagebox.showinfo('Tip', '账号或密码有误！')


    def create_interface():
        global app,show_root
        root.destroy()#关闭登录界面
        show_root=Tk()
        show_root.geometry('350x550+300+100')
        show_root.title('数据显示界面')
        app = Application(show_root)#打开显示界面
        print(id(app))
        login_done_event.set()

        show_root.mainloop()

    def click_register():   #跳转到注册页面
        register_interface(root)

    root=Tk()
    root.geometry('500x300+200+300')
    root.title('登录界面')
    '''账号'''
    label_username=Label(root,text='账号：')
    label_username.grid(row=0,column=0,padx=(150,0),pady=(50,0))
    username=StringVar()
    username.set('admin')#默认账户，加快调试
    entry_username=Entry(root,textvariable=username)
    entry_username.grid(row=0,column=1,columnspan=2,padx=10,pady=(50,0))
    '''密码'''
    label_pwd = Label(root,text='密码：')
    label_pwd.grid(row=1, column=0,padx=(150,0),pady=(10,0))
    pwd = StringVar()
    pwd.set('123')
    entry_pwd = Entry(root,textvariable=pwd)
    entry_pwd.grid(row=1, column=1,columnspan=2,padx=10,pady=(10,0))
    '''角色选择（单选按钮）'''
    label_role = Label(root, text='角色：')
    label_role.grid(row=2, column=0, padx=(150, 0), pady=(10, 0))
    global role_var
    role_var = StringVar(value='user')  # 默认选中「用户」
    rb_user = Radiobutton(root, text='用户', variable=role_var, value='user')
    rb_admin = Radiobutton(root, text='管理员', variable=role_var, value='admin')
    rb_user.grid(row=2, column=1, padx=(0, 20), pady=(10, 0))
    rb_admin.grid(row=2, column=2, pady=(10, 0))
    '''登录'''
    btn_login=Button(root,text='登录',command=click_login)
    btn_login.grid(row=3,column=1,pady=(10,0))
    '''注册'''
    btn_register = Button(root,text='注册', command=click_register)
    btn_register.grid(row=3, column=2,pady=(10,0))

    root.mainloop()

# 外部点击事件（触发返回登录界面）
def back_to_login():
    """外部点击后执行：关闭数据显示窗口，回到登录界面"""
    global show_root
    # 销毁已存在的显示窗口
    if show_root is not None and show_root.winfo_exists():
        show_root.destroy()
        show_root = None  # 重置全局变量
    # 重建登录界面
    login_interface()
'''定时设置'''

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# 定义各设备对应的命令和参数
device_config = {
    '15': {
        'commands': ['150300000002C71F'],
        'delay': 0
    },
    '16': {
        'commands': ['160300000002C72C'],
        'delay': 0.5
    },
    '79': {
        'commands': ['79032000001045BE', '790340000006DA70'],
        'delay': 1.5
    },
    '7A': {
        'commands': ['7A0320000010458D', '7A0340000006DA43'],
        'delay': 3
    },
    '06': {
        'commands': ['0603010000018441'],
        'delay': 1
    }
}

# 为每个设备创建独立的全局变量
for addr in device_config.keys():
    globals()[f"current_thread_id{addr}"] = None
    globals()[f"current_scheduler{addr}"] = None
    globals()[f"stop_flag{addr}"] = False


# 通用定时设置函数模板
def create_timing_function(addr, commands, delay):
    def timing_set(workdays, day_start, day_end, interval, app):
        # 获取设备特定的全局变量
        thread_id_name = f"current_thread_id{addr}"
        scheduler_name = f"current_scheduler{addr}"
        stop_flag_name = f"stop_flag{addr}"

        current_thread_id = globals()[thread_id_name]
        current_scheduler = globals()[scheduler_name]
        stop_flag = globals()[stop_flag_name]

        # 【核心改进1：通过线程ID强制终止旧任务（无论状态如何）】
        if current_thread_id is not None and current_scheduler is not None:
            print(f"强制终止旧任务{addr}（通过线程ID）...")
            # 1. 设置停止标志，让旧任务主动退出
            globals()[stop_flag_name] = True
            # 2. 清空旧调度器队列
            if len(current_scheduler.queue) > 0:
                current_scheduler.queue.clear()

            # 3. 向旧调度器添加空任务，强制唤醒阻塞
            def wakeup():
                pass

            try:
                current_scheduler.enter(0, 0, wakeup)
            except:
                pass
            # 4. 遍历所有活跃线程，找到旧任务线程并强制终止
            for thread in threading.enumerate():
                if thread.ident == current_thread_id and thread.is_alive():
                    print(f"发现残留的旧线程（ID: {current_thread_id}），强制终止")
                    # 注意：Python没有安全的线程终止方法，这里用标志位+超时强制隔离
                    thread.join(timeout=3)  # 等待3秒
            # 5. 重置全局状态
            globals()[thread_id_name] = None
            globals()[scheduler_name] = None
            globals()[stop_flag_name] = False
            print(f"旧任务{addr}强制清理完成")

        if interval == 0:
            '''终止节点定时'''
            return

        # ---------------- 原有配置区域 ----------------
        WORKDAYS = workdays
        DAY_START = day_start
        DAY_END = day_end
        INTERVAL = interval
        # ------------------------------------------

        # 创建新调度器
        s = sched.scheduler(time.time, time.sleep)
        globals()[scheduler_name] = s

        # 星期 -> 相对于周一的偏移
        workday_dict = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}

        def monday_obj(dt):  # 获得本周一的时间对象
            return dt - timedelta(days=dt.weekday(), hours=dt.hour, minutes=dt.minute,
                                  seconds=dt.second, microseconds=dt.microsecond)

        def generate_slots(start):  # 得到每周指定天的定时时间
            monday = monday_obj(start)
            for wd in sorted(WORKDAYS):
                day = monday + timedelta(days=workday_dict[wd])  # 本周的定时日期

                # 创建开始和结束时间对象
                start_time = day.replace(hour=DAY_START[0], minute=DAY_START[1], second=0, microsecond=0)
                end_time = day.replace(hour=DAY_END[0], minute=DAY_END[1], second=0, microsecond=0)
                while start_time <= end_time:
                    yield start_time
                    start_time += timedelta(minutes=INTERVAL)
                    # 安全检查：防止无限循环
                    if start_time > end_time + timedelta(hours=24):
                        print("检测到可能的时间计算错误，终止循环")
                        break

        # 【核心改进2：执行函数严格检查停止标志和线程ID】
        def excution_event(t):
            # 双重校验：确保当前线程是最新的，且未被标记停止
            if globals()[stop_flag_name] or threading.get_ident() != globals()[thread_id_name]:
                print(f"{addr}检测到非当前任务线程，跳过执行")
                return
            try:
                print(f"{addr}时间到了：{t.strftime('%Y-%m-%d %H:%M')}（线程ID: {globals()[thread_id_name]}）")
                # 将最新节点数据存在数据库中
                # for i, cmd in enumerate(commands):
                #     time.sleep(delay + 0.5 * i)  # 基础延迟+额外延迟
                #     data_parse([cmd])
                time.sleep(delay)
                data_parse(commands)
                # 用最新数据刷新界面
                app.refresh()
                # print("-----------与服务器建立连接---------------")
                # 只允许当前线程添加新任务
                next_t = t + timedelta(days=7)
                s.enterabs(next_t.timestamp(), 0, excution_event, argument=(next_t,))
                print('+++++++++++++++++++++++++++++执行到此----------------------')
            except Exception as e:
                print(f"任务执行出错: {e}")

        # 初始化新任务
        now = datetime.now()
        for slot in generate_slots(now):
            if slot >= now:
                s.enterabs(slot.timestamp(), 0, excution_event, argument=(slot,))
        print(f"{addr}新调度器已启动，等待触发…")

        # 【核心改进3：记录新线程ID，确保唯一】
        def run_scheduler():
            globals()[thread_id_name] = threading.get_ident()  # 记录当前线程ID
            s.run()

        # 启动新线程
        new_thread = threading.Thread(target=run_scheduler, daemon=True)
        new_thread.start()

    return timing_set


# 为每个设备动态创建定时设置函数
for addr, config in device_config.items():
    func_name = f"timing_set{addr}"
    globals()[func_name] = create_timing_function(addr, config['commands'], config['delay'])

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



'''--------------timingxx()：检查文件定时数据，并开始定时------------'''
#登录&注册界面

'''根据addr动态生成生成一个 timingXX 函数'''
def make_timing_function(addr):
    def timing_func():
        # 每个函数有自己的状态（通过闭包）
        last_info = None
        last_mtime = 0

        filepath = f'../info_timing/info_{addr}.txt'
        set_func_name = f'timing_set{addr}'
        set_func = globals().get(set_func_name)

        if set_func is None or not callable(set_func):
            print(f"错误：未找到定时设置函数 {set_func_name}")
            return

        def check_and_reload():
            nonlocal last_info, last_mtime
            try:
                current_mtime = os.path.getmtime(filepath)
                if current_mtime == last_mtime:
                    return False

                with open(filepath, 'r') as f:
                    current_info = f.read()

                if current_info == last_info:
                    last_mtime = current_mtime
                    return False

                last_info = current_info
                last_mtime = current_mtime
                return True

            except FileNotFoundError:
                print(f"info_{addr}.txt 文件不存在")
                return False
            except Exception as e:
                print(f"读取文件出错: {e}")
                return False

        # 主循环
        while True:
            if check_and_reload():

                print(f"{addr}检测到文件内容变化，重新加载定时设置...")
                info = last_info

                if info != '':
                    try:
                        timing_data = time_parse(info)
                        day_start = (timing_data[0], timing_data[1])
                        day_end = (timing_data[2], timing_data[3])
                        workdays = timing_data[4]
                        interval = timing_data[5]
                        print(f"新定时参数: {workdays}, {day_start}-{day_end}, 间隔{interval}分钟")
                        set_func(workdays, day_start, day_end, interval, app)
                    except Exception as e:
                        print(f"解析定时数据出错: {e}")
                else:
                    set_func(0, 0, 0, 0, app)

            time.sleep(5)

    return timing_func

def run_timing():
    addr_list=read_sensor_addr_info()+read_power_addr_info()+['06']
    threading.Thread(target=login_interface, daemon=True).start()
    if login_done_event.wait(timeout=30):
        # 动态生成 timing15, timing16, timing79... 等函数，并放入全局作用域
        for addr in addr_list:
            func_name = f'timing{addr}'
            globals()[func_name] = make_timing_function(addr)


        #调用timing15,timing16...函数
        for addr in addr_list:
            func_name = f"timing{addr}"
            func=globals()[func_name]
            threading.Thread(target=func, daemon=True).start()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if __name__ == '__main__':
    root = Tk()
    root.geometry('350x500+300+100')
    root.title('数据显示界面')
    app = Application(root)

    timing_data = time_parse("DDEEFF15080017007D78")
    day_start = (timing_data[0], timing_data[1])
    day_end = (timing_data[2], timing_data[3])
    workdays = timing_data[4]
    interval = timing_data[5]
    # timing_set15(workdays, day_start, day_end, interval, app)
    root.mainloop()
