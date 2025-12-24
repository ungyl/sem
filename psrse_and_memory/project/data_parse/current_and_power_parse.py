# -*- coding: utf-8 -*-
#创建时间：2025/9/20 17:27
'''获得电流和功率'''
def get_current_power(client_req,server_resp):
    def binary_fraction_to_decimal(binary_str): #将二进制小数字符串转换为十进制
        total = 0.0
        for i, bit in enumerate(binary_str, 1):
            if bit == '1':
                total += 2 ** (-i)  # 第i位乘以2^(-i)
        return total
    def calculate_electric_energy(hex_str):
        decimal_num=int(hex_str,16)
        binary_str=bin(decimal_num)[2:]
        if len(binary_str)<32:          #保证binary_str为32位，不足在前面补0
            x=32-len(binary_str)
            add_0=''
            for i in range(x):
                add_0+='0'
            binary_str=add_0+binary_str
        sign=int(binary_str[0],2)   #符号位 1位
        S=(-1)**sign                #公式中的 S
        e=int(binary_str[1:9],2)-127    #公式中的e  指数位 8位
        M=binary_str[9:]                #尾数位 23位
        M_full=1+binary_fraction_to_decimal(M) #公式中的M_full
        return S*(2**e)*M_full                 #计算公式

    # client_req= '790340000006DA70'   #'7A0340000006DA43'     #客户发送的数据
    # server_resp='79030C3D8F5C293D8F5C290000000002E7'    #'7A030C3E23D70A3E23D70A0000000074EF'    #服务器响应数据
    lst_byte_client_req = [client_req[i:i + 2] for i in range(0, len(client_req), 2)] #每个元素都是一个字节
    lst_byte_server_resp=[server_resp[i:i + 2] for i in range(0, len(server_resp), 2)]
    current=''.join(lst_byte_server_resp[7:11])    #得到电能值表达式0x3E23D70A
    current=calculate_electric_energy(current)
    power=''.join(lst_byte_server_resp[11:15])
    power = calculate_electric_energy(power)
    return current,power
if __name__ == '__main__':
    current,power=get_current_power('79032000001045BE','790320435D4CCD3CE560423BCE703B'
                                                 '000000003BCE703B3F800000000000004247EB85CBED')

    print(current)
    print(power)