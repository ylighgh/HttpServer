#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import ssl
import argparse
import socket
from urllib.parse import urlparse

menu = argparse.ArgumentParser(description='Purl')
menu.add_argument('--data', '-D', help='POST请求的数据')
menu.add_argument('--method', '-X', help='请求的动作(GET,POST,DELETE)', default='GET')
menu.add_argument('--header', '-H', help='自定义请求头 例如:application/json', default='text/html')
menu.add_argument('--url', '-U', help='需要访问的地址，必要参数')
menu.add_argument('--proxy', '-P', help='设置代理地址 只支持Http代理 例如:http://127.0.0.1:1080')
option = menu.parse_args()


class Request:
    """
    请求报文数据
    """
    scheme = ''
    method = ''
    uri = ''
    version = 'HTTP/1.1'
    ip = ''
    port = 0
    content_type = ''
    content_length = ''
    request_body = ''
    proxy_ip = ''
    proxy_port = 0

    def get_ip_port(self, my_option: object):
        """
        获取远程主机和端口号
        """
        connect = urlparse(my_option.url)
        self.scheme = connect.scheme
        self.ip = connect.hostname
        if connect.path != '':
            self.uri = connect.path
        else:
            self.uri = '/'
        if self.scheme == 'https' and None == connect.port:
            self.port = 443
        elif self.scheme == 'http' and None == connect.port:
            self.port = 80
        else:
            self.port = connect.port
        proxy = urlparse(my_option.proxy)
        if None != proxy.hostname:
            self.proxy_ip = proxy.hostname
            self.proxy_port = proxy.port

    def __init__(self, method: str, content_type: str, request_body: str):
        self.method = method
        self.get_ip_port(option)
        self.content_type = content_type
        if method == 'POST':
            self.content_length = len(request_body)
            self.request_body = request_body


def build_request_message(request: object):
    """
    构建请求报文
    """
    if request.method == 'GET' or request.method == 'DELETE':
        return (f'{request.method} {request.uri} {request.version}\r\n'
                f'Host: {request.ip}:{request.port}\r\n'
                f'Content-Type: {request.content_type}\r\n\r\n')
    else:
        return (f'{request.method} {request.uri} {request.version}\r\n'
                f'Host: {request.ip}:{request.port}\r\n'
                f'Content-Length: {request.content_length}\r\n'
                f'Content-Type: {request.content_type}\r\n\r\n'
                f'{request.request_body}')


def http_connect_server(my_option: object, request_data: str):
    """
    http方式连接服务器
    """
    if 0 != my_option.proxy_port:
        remote_ip = my_option.proxy_ip
        remote_port = my_option.proxy_port
        print('正在使用代理,端口为:' + remote_ip + ":" + str(remote_port))
    else:
        remote_ip = my_option.ip
        remote_port = my_option.port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_ip, remote_port))
    s.send(request_data.encode("utf-8"))
    data = s.recv(2048)
    print(data.decode('utf-8'))
    s.close()


def https_connect_server(my_option: object, request_data: str):
    """
    https方式连接服务器
    """
    remote_ip = my_option.ip
    remote_port = my_option.port
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    with context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=remote_ip) as s:
        s.connect((remote_ip, remote_port))
        s.send(request_data.encode("utf-8"))
        data = s.recv(2048)
        print(data.decode('utf-8'))


def main():
    request_obj = Request(option.method, option.header, option.data)
    request_data = build_request_message(request_obj)
    if request_obj.scheme == 'http':
        http_connect_server(request_obj, request_data)
    else:
        https_connect_server(request_obj, request_data)


if __name__ == '__main__':
    main()
