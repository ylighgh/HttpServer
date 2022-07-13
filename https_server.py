#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import ssl
import socket


class Response:
    """
    响应报文数据
    """
    version = 'HTTP/1.1'
    code = ''
    status = ''
    content_Length = ''
    content_Type = ''
    server = ''
    response_Body = ''

    def __init__(self, code: str, status: str, content_Length: str, response_Body: str):
        self.code = code
        self.status = status
        self.content_Length = content_Length
        self.content_Type = 'text/html'
        self.server = 'nginx/1.20.2'
        self.response_Body = response_Body


def build_response_message(response: object):
    """
    构建响应报文
    """
    return (f'{response.version} {response.code} {response.status}\r\n'
            f'Content-Length: {response.content_Length}\r\n'
            f'Content-Type: {response.content_Type}\r\n'
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
    sock.bind(('127.0.0.1', 8081))
    sock.listen(5)
    ssock = context.wrap_socket(sock, server_side=True)
    return ssock


def get_resopnse_message():
    """
    获取响应报文
    """
    with open('./index.html', encoding='utf-8') as success_file:
        success_content = success_file.read()
        success_response = build_response_message(Response('200', 'OK', str(len(success_content)), success_content))
    with open('./404.html', encoding='utf-8') as failed_file:
        failed_content = failed_file.read()
        failed_response = build_response_message(Response('404', 'NOT FOUND', str(len(failed_content)), failed_content))
    return success_response, failed_response


def connect_client(s: object):
    """
    传输数据
    """
    success_response, failed_response = get_resopnse_message()
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            uri = conn.recv(1024).decode('utf-8').split()[1]
            if uri == '/':
                conn.send(success_response.encode("utf-8"))
            else:
                conn.send(failed_response.encode('utf-8'))


def close_server(s: object):
    """
    断开连接
    """
    s.close()


def main():
    s = create_server()
    connect_client(s)
    close_server(s)


if __name__ == '__main__':
    main()
