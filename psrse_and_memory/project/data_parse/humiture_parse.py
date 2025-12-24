# -*- coding: utf-8 -*-
#创建时间：2025/8/30 8:47
def get_humiture(client_req,server_resp):
    def is_humiture_parse(send,recv):
        if send[0:2]!=recv[0:2] or len(recv)!=5+int(recv[2],16):    #前两个字节是否相同;是否满足条件：L=5+p3
            print('温湿度校验失败！')
            exit(0)
        return True

    # client_req= '160300000002C72C'   #'150300000002C71F'      #客户发送的数据
    # server_resp='16030401EC013F1CBB'#'150304020100C4FFD9'    #服务器响应数据
    lst_byte_client_req = [client_req[i:i + 2] for i in range(0, len(client_req), 2)] #每个元素都是一个字节
    lst_byte_server_resp=[server_resp[i:i + 2] for i in range(0, len(server_resp), 2)]
    if is_humiture_parse(lst_byte_client_req,lst_byte_server_resp):
        humidity=str(int(lst_byte_server_resp[3]+lst_byte_server_resp[4],16))
        humidity=humidity[:-1]+'.'+humidity[-1]+'%'
        temperature=str(int(lst_byte_server_resp[5]+lst_byte_server_resp[6],16))
        temperature=temperature[:-1]+'.'+temperature[-1]+'℃'
    return humidity,temperature
if __name__ == '__main__':
    hum,tem=get_humiture('160300000002C72C','16030401EC013F1CBB')
    print(hum,tem)