# -*- coding: utf-8 -*-
#创建时间：2025/10/4 11:21 
def time_parse(client_req):
    timing_data=[]
    def add_to_8(day_bin):# 保证day_bin为8位，不足在前面补0
        if len(day_bin) < 8:
            x = 8 - len(day_bin)
            add_0 = ''
            for i in range(x):
                add_0 += '0'
            day_bin_str = add_0 + day_bin
        return day_bin_str

    def bits_to_set(bin_str):#将设置的时间以集合形式显示
        s=set()
        for i, bit in enumerate(reversed(bin_str),1):
            if bit=='1':
                s.add(i)
        return s

    lst_byte_client_req = [client_req[i:i + 2] for i in range(0, len(client_req), 2)] #每个元素都是一个字节

    #起始时间       时，分
    begin_hour_hex=lst_byte_client_req[4]
    begin_hour_decimal=int(begin_hour_hex,16)# 16 进制转 10 进制
    timing_data.append(begin_hour_decimal)      #起始时间
    begin_minute_hex=lst_byte_client_req[5]
    begin_minute_decimal=int(begin_minute_hex,16)
    timing_data.append(begin_minute_decimal)    #起始时间
    #终止时间       时，分
    end_hour_hex=lst_byte_client_req[6]
    end_hour_decimal=int(end_hour_hex,16)
    timing_data.append(end_hour_decimal)    #终止时间
    end_minute_hex=lst_byte_client_req[7]
    end_minute_decimal=int(end_minute_hex,16)
    timing_data.append(end_minute_decimal)  #终止时间
    #每周情况  1-7天
    day_hex=lst_byte_client_req[8]
    day_bin=bin(int(day_hex,16))[2:]#得到 2 进制数
    day_bin_8=add_to_8(day_bin)
    set_day=bits_to_set(day_bin_8)
    timing_data.append(set_day)     #一周的哪几天
    #刷新间隔   单位 ：分钟  1-120
    interval_hex=lst_byte_client_req[9]
    interval_decimal=int(interval_hex,16)
    timing_data.append(interval_decimal)    #时间间隔
    return timing_data
if __name__ == '__main__':
    client_req = "DDEEFF15080014007D78"
    timing_data=time_parse(client_req)
    print(timing_data)
