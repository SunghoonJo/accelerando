import socket, select

from io import StringIO
from accelerando.dispatcher import Dispatcher

class EPollDispatcher(Dispatcher):

	def initialize(self):
		self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._serversocket.bind((self.hostname, self.port))
		self._serversocket.listen(self.backlog)
		self._serversocket.setblocking(0)
		
		self._epoll = select.epoll()
		self._epoll.register(self._serversocket.fileno(), select.EPOLLIN)

		self._connections = {}
		self._processors = {}
	def dispatch_and_handle(self, processor_class):
		if not processor_class:
			raise Exception("TCPProcessor is None is None")
		try:
			while True:
				events = self._epoll.poll(1)
				for fileno, event in events:
					if fileno == self._serversocket.fileno():
						connection, address = self._serversocket.accept()
						connection.setblocking(0)
						self._epoll.register(connection.fileno(), select.EPOLLIN)

						self._connections[connection.fileno()] = connection
						self._processors[connection.fileno()] = processor_class(address)
					elif event & select.EPOLLIN:
						connection = self._connections[fileno]
						processor = self._processors[fileno]
						processor.initialize()
						try:
							while True:	
								buffer_in = connection.recv(4096)
								if not buffer_in or buffer_in == b'':
									break
								processor.receive_request(buffer_in)
						except socket.error:
							pass
						self._epoll.modify(fileno, select.EPOLLOUT)
					elif event & select.EPOLLOUT:
						connection = self._connections[fileno]
						processor = self._processors[fileno]
						
						response = processor.handle_request()
						if not response:
							response = b''
						byteswritten = connection.send(response)
						response = response[byteswritten:]
						if len(response) == 0:
							self._epoll.modify(fileno, select.EPOLLHUP)
							connection.shutdown(socket.SHUT_RDWR)
					elif event & select.EPOLLHUP:
						self._epoll.unregister(fileno)
						self._connections[fileno].close()
						del self._processors[fileno]
		except KeyboardInterrupt:
			print("Keyboard Interrupt")

	def finalize(self):
		self._epoll.unregister(self._serversocket.fileno())
		self._epoll.close()
		self._serversocket.close()
