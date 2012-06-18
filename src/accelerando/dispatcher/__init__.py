
class Dispatcher(object):

	def __init__(self, hostname, port, backlog, application_context):
		self.hostname = hostname
		self.port = port
		self.backlog = backlog
		self.application_context = application_context

	def initialize(self):
		pass
	
	def dispatch_and_handle(self, tcp_handler):
		pass

	def finalize(self):
		pass
		
from accelerando.dispatcher.py_async import PythonAsyncCoreDispatcher
from accelerando.dispatcher.epoll import EPollDispatcher
