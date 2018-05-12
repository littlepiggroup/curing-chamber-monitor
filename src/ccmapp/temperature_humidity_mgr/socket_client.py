# -*- coding: utf-8 -*-

## Only for test. Can remove this file in production.

import socket

import time

if __name__ == '__main__':

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # clientsocket.connect(('139.196.195.8', 8899))
    clientsocket.connect(('127.0.0.1', 8899))

    try:
        while True:
            data = '\x01\x01\x04\x01\x08\x01\x81\xAB\x3D'
            # data = '\x01\x01\x04\x01'
            print type(data)
            clientsocket.send(data)
            time.sleep(5)
    except Exception, e:
        clientsocket.close()