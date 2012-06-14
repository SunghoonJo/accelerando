import asyncore
import socket

from accelerando.dispatcher import Dispatcher

class PythonAsyncCoreDispatcher(Dispatcher):
	class Instance(asyncore.dispatcher):
		def handle_accept(self):
			socket, address = self.accept()
			if socket is None:
				pass
			elif self.accept_handler_class is None:
				pass
			else:
				handler = self.accept_handler_class()
				socket.setblocking(0)
				handler(socket, address)

	def __init__(self, hostname, port, backlog):
		asyncore.dispatcher.__init__(self)

		self.instance = self.Instance()
		self.instance.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.instance.set_reuse_addr()
		self.instance.bind((hostname, port))
		self.instance.listen(backlog)

	def __call__(self, accept_handler_class):
		self.instance.accept_handler_class = accept_handler_class
		
#asyncore.loop()

