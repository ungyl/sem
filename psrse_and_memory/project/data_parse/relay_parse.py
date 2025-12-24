# -*- coding: utf-8 -*-
#创建时间：2025/8/30 18:34

'''查看1-8路 或 9-16路 继电器开关状态'''
def check_relay_state(client_req,server_resp):
    def is_relay_parse(send,recv):
        if send[0:2] != recv[0:2] or len(recv) != 5 + int(recv[2], 16):  # 前两个字节是否相同;是否满足条件：L=5+p3
            print('查看继电器状态校验失败！')
            exit(0)
        return True

    # client_req= '09030100000184BE'   #'150300000002C71F'      #客户发送的数据
    # server_resp='09030200005985'#'150304020100C4FFD9'    #服务器响应数据
    lst_byte_client_req = [client_req[i:i + 2] for i in range(0, len(client_req), 2)]  # 每个元素都是一个字节
    lst_byte_server_resp = [server_resp[i:i + 2] for i in range(0, len(server_resp), 2)]
    if is_relay_parse(lst_byte_client_req,lst_byte_server_resp):#判断校验
        relay_state_hex=lst_byte_server_resp[4]     #这里只取了数据为中的有效位
        relay_state_binary=format(int(relay_state_hex,16),'08b')#b 表示二进制。08 表示字符串总长度为 8，不足部分用 0 填充在左侧。
        relay_state_lst=relay_state_binary.replace('1','开').replace('0','关')#获得8路继电器状态
        return relay_state_lst

'''更改1-16路继电器开关状态'''
def change_relay_state(client_req,server_resp):
    def is_relay_parse(send,recv):
        if send[0:6]==recv[0:6] and len(recv)==8:
            return True
        else:
            print('修改继电器校验失败！')
            exit(0)

    lst_byte_client_req = [client_req[i:i + 2] for i in range(0, len(client_req), 2)]  # 每个元素都是一个字节
    lst_byte_server_resp = [server_resp[i:i + 2] for i in range(0, len(server_resp), 2)]
    if is_relay_parse(lst_byte_client_req,lst_byte_server_resp):
        '''1-8路的关闭操作'''
        down_1_to_8_hex=lst_byte_client_req[8]      #1-8路关闭操作的16进制表达
        down_1_to_8_binary=format(int(down_1_to_8_hex,16),'08b')##1-8路关闭操作的2进制表达
        down_1_to_8_binary=down_1_to_8_binary[::-1]
        down_1_to_8_lst=[]              #存储1-8路继电器哪一路执行关闭操作
        for i, bit in enumerate(down_1_to_8_binary,1):
            if bit=='1':
                down_1_to_8_lst.append(i)
        '''9-16路的关闭操作'''
        down_9_to_16_hex = lst_byte_client_req[10]  # 9-16路关闭操作的16进制表达
        down_9_to_16_binary = format(int(down_9_to_16_hex, 16), '08b')  ##9-16路关闭操作的2进制表达
        down_9_to_16_lst = []  # 存储9-16路继电器哪一路执行关闭操作
        for i, bit in enumerate(down_9_to_16_binary, 9):
            if bit == '1':
                down_9_to_16_lst.append(i)
        '''1-8路的打开操作'''
        up_1_to_8_hex = lst_byte_client_req[12]  # 1-8路打开操作的16进制表达
        up_1_to_8_binary = format(int(up_1_to_8_hex, 16), '08b')  ##1-8路打开操作的2进制表达
        up_1_to_8_binary=up_1_to_8_binary[::-1]
        up_1_to_8_lst = []  # 存储1-8路继电器哪一路执行打开操作
        for i, bit in enumerate(up_1_to_8_binary, 1):
            if bit == '1':
                up_1_to_8_lst.append(i)
        '''9-16路的打开操作'''
        up_9_to_16_hex = lst_byte_client_req[14]  # 9-16路打开操作的16进制表达
        up_9_to_16_binary = format(int(up_9_to_16_hex, 16), '08b')  ##9-16路打开操作的2进制表达
        up_9_to_16_lst = []  # 存储9-16路继电器哪一路执行打开操作
        for i, bit in enumerate(up_9_to_16_binary, 9):
            if bit == '1':
                up_9_to_16_lst.append(i)
    return down_1_to_8_lst,down_9_to_16_lst,up_1_to_8_lst,up_9_to_16_lst

def send_relay_change_state(info):
    down_1_to_8_lst,down_9_to_16_lst,up_1_to_8_lst,up_9_to_16_lst=change_relay_state(info,'0610010200046041')#接收消息仅供校验，这里为了方便，固定
    server_data = ''
    if not (down_1_to_8_lst or up_1_to_8_lst):  # 没有任何操作
        server_data += "no change"
    if not down_1_to_8_lst:  # 无关闭操作
        pass
    else:
        server_data += ','.join(map(str, down_1_to_8_lst)) + " turn down "
    if not up_1_to_8_lst:  # 无关闭操作
        pass
    else:
        server_data += ','.join(map(str, up_1_to_8_lst)) + " turn up"

    return server_data


if __name__ == '__main__':

    state = change_relay_state('0610010200040800000000000100005BFE','0610010200046041')
    print(state)


