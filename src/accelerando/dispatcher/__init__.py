
class Dispatcher(object):
	def __call__(self, hostname, port, backlog, tcp_handler):
		return
		
from accelerando.dispatcher.py_async import PythonAsyncCoreDispatcher
from accelerando.dispatcher.epoll import EPollDispatcher
