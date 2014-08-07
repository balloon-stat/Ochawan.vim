#! /usr/bin/python
# -*- encoding: utf-8 -*-

import struct
import socket

class Bouyomi:
    def __init__(self):
        self.code    = 0
        self.voice   = 1
        self.volume  = -1
        self.speed   = -1
        self.tone    = -1
        self.command = 0x0001

    def header(self, text):
        length = len(text)
        return struct.pack( '5hbi',
                            self.command,
                            self.speed,
                            self.tone,
                            self.volume,
                            self.voice,
                            self.code,
                            length )

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 50001))

    def send(self, text):
        self.sock.sendall(self.header(text))
        self.sock.sendall(text)

    def close(self):
        self.sock.close()
