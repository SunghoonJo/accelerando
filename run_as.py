#!/usr/bin/env python3

import os, sys, imp

sys.path.append(os.getcwd() + "/src")

from accelerando.tcp_server import TCPServer
from accelerando.handler.http import HTTPHandler

server = TCPServer('localhost', 3000)
server.init()
server.run(HTTPHandler)
