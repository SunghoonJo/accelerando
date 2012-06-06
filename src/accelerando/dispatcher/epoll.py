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
			while True:
				events = epoll.poll(1)
				for fileno, event in events:
					if fileno == serversocket.fileno():
					elif event & select.EPOLLIN:
					elif event & select.EPOLLOUT:
		finally:
			epoll.unregister(serversocket.fileno())
			epoll.close()
			serversocket.close()
