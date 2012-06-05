#!/usr/bin/env python3

import os, sys, imp

sys.path.append(os.getcwd() + "/src")

from accelerando.tcp_server import TCPServer

server = TCPServer('localhost', 3000)
server.init()
server.run()
