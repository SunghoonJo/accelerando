from accelerando.dispatcher import *
from accelerando.handler import *

class TCPServer(object):

	def __init__(self, host, port, backlog=20, dispatcher_class=PythonAsyncCoreDispatcher):
		self.host = host
		self.port = port
		self.backlog = backlog
		self.dispatcher_class = dispatcher_class

	def init(self):
		self.dispatcher = self.dispatcher_class(self.host, self.port, self.backlog)
		if self.dispatcher is None:
			raise Exception

	def run(self, accept_handler=SimpleReactTCPHandler):
		if accept_handler is None:
			raise Exception
		if self.dispatcher is None:
			raise Exception
		self.dispatcher(accept_handler)
