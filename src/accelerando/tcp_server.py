from accelerando.dispatcher import *
from accelerando.handler import *

class TCPServer(object):

	def __init__(self, hostname, port, backlog=20, dispatcher_class=PythonAsyncCoreDispatcher):
		self.hostname = hostname
		self.port = port
		self.backlog = backlog
		self.dispatcher_class = dispatcher_class
	
	def init(self):
		if not self.dispatcher_class:
			raise Exception
		self.dispatcher = self.dispatcher_class()

	def run(self, tcp_handler=SimpleReactTCPHandler):
		if not tcp_handler:
			raise Exception
		if not self.dispatcher:
			raise Exception
		self.dispatcher(self.hostname, self.port, self.backlog, tcp_handler)
