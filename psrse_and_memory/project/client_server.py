# -*- coding: utf-8 -*-
#创建时间：2025/8/30 8:48 
def connect_server(client_req):
    import socket
    client_socket=socket.socket()
    ip='192.168.137.1'   #
    port=55900          #8080
    client_socket.connect((ip,port))
    print('-----------与服务器建立连接---------------')
    data=bytes.fromhex(client_req)          #将16进制字符串转换为b'\x15\x03\x00\x00\x00\x02\xc7\x1f'
    client_socket.send(data)                        #向服务器发送数据
    info=client_socket.recv(1024).hex().upper()     #接收服务器返回的数据
    print('客户端发送的数据：{}'.format(client_req))
    print('服务器响应的数据：{}'.format(info))
    print('------------与服务器断开连接---------------')
    client_socket.close()                           #关闭客户端连接
    return info
if __name__ == '__main__':
    client_req='0603010000018441'
    server_resp=connect_server(client_req)
    print(server_resp)