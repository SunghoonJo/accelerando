#!/usr/bin/env python3

import os, sys

sys.path.append(os.getcwd() + "/src")

from accelerando.tcp import TCPServer
from accelerando.processor.http import HTTPProcessor
from accelerando.dispatcher import EPollDispatcher

server = TCPServer('localhost', 3000, 20, EPollDispatcher)
server.run(HTTPProcessor)
