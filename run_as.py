#!/usr/bin/env python3

import os, sys

sys.path.append(os.getcwd() + "/src")

from accelerando.tcp_server import TCPServer
from accelerando.handler.http import HTTPHandler
from accelerando.dispatcher import EPollDispatcher

server = TCPServer('localhost', 3000, 20, EPollDispatcher)
server.init()
server.run(HTTPHandler)
