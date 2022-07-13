#!/usr/bin/env python3
# -*- coding:utf-8 -*-
def get_response_message(s):
    """
    获取响应报文
    """
    total_data = []
    while True:
        data = s.recv(20480)
        if not data:
            break
        total_data.append(data.decode('utf-8'))
    return ''.join(total_data)