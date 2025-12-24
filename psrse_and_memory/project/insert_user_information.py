# -*- coding: utf-8 -*-
#创建时间：2025/9/5 10:54
from tkinter import messagebox
from project.database_configure import database_configure
'''insert_user_data(new_username,new_pwd,role_state):根据当前选择的角色状态进行注册'''
def insert_user_data(new_username,new_pwd,role_state):
    cursor,user_result,con,admin_result= database_configure()
    if role_state=='user':
        if user_result!=():#有数据情况，要检查账号是否存在
            usernames = [data[0] for data in user_result]    #得到一个所有账号的列表
            pwds=[data[1] for data in user_result]
            if new_username not in usernames and new_username!='':
                cursor.execute('insert into t_user_data(username,pwd) values (%s,%s)',args=(new_username,new_pwd))
                messagebox.showinfo('提示', '注册成功！')
            else:messagebox.showinfo('提示','创建失败，账号已存在！')
        else:#无数据情况，直接添加
            cursor.execute('insert into t_user_data(username,pwd) values (%s,%s)',args=(new_username,new_pwd))
            messagebox.showinfo('提示', '注册成功！')
    elif role_state=='admin':
        if admin_result!=():#有数据情况，要检查账号是否存在
            usernames = [data[0] for data in admin_result]    #得到一个所有账号的列表
            pwds=[data[1] for data in admin_result]
            if new_username not in usernames and new_username!='':
                cursor.execute('insert into t_admin_data(username,pwd) values (%s,%s)',args=(new_username,new_pwd))
                messagebox.showinfo('提示', '注册成功！')
            else:messagebox.showinfo('提示','创建失败，账号已存在！')
        else:#无数据情况，直接添加
            cursor.execute('insert into t_admin_data(username,pwd) values (%s,%s)',args=(new_username,new_pwd))
            messagebox.showinfo('提示', '注册成功！')

if __name__ == '__main__':
    insert_user_data('','123')





