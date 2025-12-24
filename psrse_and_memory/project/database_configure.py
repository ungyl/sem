# -*- coding: utf-8 -*-
#创建时间：2025/9/5 10:22 
from pymysql import Connection
def database_configure():
    # 创建数据库连接
    con = Connection(
        host='localhost',
        port=3306,
        user='root',
        password='123456789',
        database='sql_test1',  # 所操作数据库的名称
        autocommit=True  # 自动提交，而不用每次执行DML语句后额外写con.commit
    )
    cursor = con.cursor()  # 创建游标对象
    user_sql = '''
                create table if not exists t_user_data(
                username varchar(255) primary key,
                pwd varchar(255)
                ) engine=InnoDB default charset=utf8;
                '''
    admin_sql = '''
                    create table if not exists t_admin_data(
                    username varchar(255) primary key,
                    pwd varchar(255)
                    ) engine=InnoDB default charset=utf8;
                    '''
    cursor.execute(user_sql)  # 创建普通用户表
    cursor.execute(admin_sql)  # 创建管理员表

    cursor.execute('select * from t_user_data')
    user_result = cursor.fetchall()

    cursor.execute('select * from t_admin_data')
    admin_result = cursor.fetchall()

    return cursor,user_result,con,admin_result

if __name__ == '__main__':

    res1,res2 = database_configure()[1],database_configure()[3]
    print(res1,res2)