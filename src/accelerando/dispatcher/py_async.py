import asyncore
import socket

from accelerando.dispatcher import Dispatcher

class PythonAsyncCoreDispatcher(Dispatcher, asyncore.dispatcher):
	def __init__(self, hostname, port, backlog):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((hostname, port))
		self.listen(backlog)

	def handle_accept(self):
		sockAndAddress = self.accept()
		if sockAndAddress is None:
			pass
		else:
			socket, address = sockAndAddress
			if self.accept_handler is None:
				pass
			else:
				handler = self.accept_handler(socket, address)
				handler.execute()

		pass

	def dispatch_loop(self, accept_handler):
		self.accept_handler = accept_handler

		asyncore.loop()

