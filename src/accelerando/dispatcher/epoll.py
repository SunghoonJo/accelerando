import socket, select

from accelerando.dispatcher import Dispatcher

class EPollDispatcher(Dispatcher):
	def __init__(self, hostname, port, backlog):
		self.hostname = hostname
		self.port = port
		self.backlog = backlog

	def __call__(self, accept_handler_class):
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind((self.hostname, self.port))
		serversocket.listen(self.backlog)
		serversocket.setblocking(0)

		epoll = select.epoll()
		epoll.register(serversocket.fileno(), select.EPOLLIN)
		try:
			connections = {};
			while True:
				events = epoll.poll(1)
				for fileno, event in events:
					if fileno == serversocket.fileno():
						connection, address = serversocket.socket.accept()
						connection.setblocking(0)
						epoll.register(connection.fileno(), select.EPOLLIN)
						connections[connection.fileno()] = connection
					elif event & select.EPOLLIN:
					elif event & select.EPOLLOUT:
					elif event & select.EPOLLHUP:
					 epoll.unregister(fileno)
					 connections[fileno].close()
					 del connections[fileno]
		finally:
			epoll.unregister(serversocket.fileno())
			epoll.close()
			serversocket.close()
