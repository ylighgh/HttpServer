#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import ssl
import base64
import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_sock = client_socket
        print("New connection added: ", client_address)

    def run(self):
        file_name = ''
        file_extension = ''
        try:
            file_name = (self.client_sock.recv(1024).decode('utf-8').split('/')[1]).split()[0]
            file_extension = file_name.split('.')[1]
        except IndexError:
            self.client_sock.send(get_resopnse_message('index.html', 'text/html').encode("utf-8"))
        try:
            if file_extension == 'html':
                self.client_sock.send(get_resopnse_message(file_name, 'text/html').encode("utf-8"))
            elif file_extension == 'json':
                self.client_sock.send(get_resopnse_message(file_name, 'application/json').encode("utf-8"))
            elif file_extension == 'xml':
                self.client_sock.send(get_resopnse_message(file_name, 'text/xml').encode("utf-8"))
            elif file_extension == 'jpg':
                try:
                    resopnse_body = read_img(file_name)
                    self.client_sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
                    self.client_sock.send(resopnse_body)
                except FileNotFoundError:
                    self.client_sock.send(get_resopnse_message('404.html', 'text/html').encode("utf-8"))
            else:
                self.client_sock.send(get_resopnse_message('404.html', 'text/html').encode("utf-8"))
        except FileNotFoundError:
            self.client_sock.send(get_resopnse_message('404.html', 'text/html').encode("utf-8"))


class Response:
    """
    响应报文数据
    """
    version = 'HTTP/1.1'
    code = ''
    status = ''
    content_length = ''
    content_type = ''
    server = ''
    response_Body = ''

    def __init__(self, code: str, status: str, content_length: str, content_type: str, response_Body: str):
        self.code = code
        self.status = status
        self.content_length = content_length
        self.content_type = content_type
        self.server = 'nginx/1.20.2'
        self.response_Body = response_Body


def build_response_message(response: object):
    """
    构建响应报文
    :param response: 请求报文的类对象
    """
    return (f'{response.version} {response.code} {response.status}\r\n'
            f'Content-Length: {response.content_length}\r\n'
            f'Content-Type: {response.content_type}\r\n'
            f'Server: {response.server}\r\n\r\n'
            f'{response.response_Body}')


def create_server():
    """
    建立连接
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('/home/ylighgh/workspace/software/yssuvu.xyz/fullchain.pem',
                            '/home/ylighgh/workspace/software/yssuvu.xyz/privkey.pem')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.2.161', 8081))
    sock.listen(5)
    ssock = context.wrap_socket(sock, server_side=True)
    return ssock


def read_img(file_path):
    """
    读取图片数据
    :param file_path: 文件的路径
    """
    file = open(file_path, 'rb')
    file_data = file.read()
    file.close()
    return file_data


def get_resopnse_message(file_name: str, content_type: str):
    """
    获取响应报文
    :param file_name: 文件名
    :param content_type: 文件传输的类型
    """
    if content_type == 'image/jpg':
        response = build_response_message(
            Response('200', 'OK', 0, content_type, ''))
    else:
        with open(file_name, encoding='utf-8') as success_file:
            content = success_file.read()
            response = build_response_message(
                Response('200', 'OK', str(len(content)), content_type, content))
    return response


def connect_client(s: object):
    """
    连接客户端
    :param s: socket对象
    """
    while True:
        client_sock, client_address = s.accept()
        new_thread = ClientThread(client_address, client_sock)
        new_thread.run()


def close_server(s: object):
    """
    断开与socket的连接
    :param s: socket对象
    """
    s.close()


def main():
    s = create_server()
    connect_client(s)
    close_server(s)


if __name__ == '__main__':
    main()
