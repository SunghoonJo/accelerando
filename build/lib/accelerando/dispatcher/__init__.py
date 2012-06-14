
class Dispatcher(object):

	def __init__(self, hostname, port, backlog):
		self.hostname = hostname
		self.port = port
		self.backlog = backlog

	def initialize(self):
		pass
	
	def dispatch_and_handle(self, tcp_handler):
		pass

	def finalize(self):
		pass
		
from accelerando.dispatcher.py_async import PythonAsyncCoreDispatcher
from accelerando.dispatcher.epoll import EPollDispatcher
