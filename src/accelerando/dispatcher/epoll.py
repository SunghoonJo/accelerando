import socket, select

from accelerando.tcp import TCPRequest, TCPResponse
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
		self._requests = {}
		self._responses = {}

	def dispatch_and_handle(self, tcp_handler):
		if not tcp_handler:
			raise Exception("TCPHandler is None")

		while True:
			events = self._epoll.poll(1)
			for fileno, event in events:
				if fileno == self._serversocket.fileno():
					connection, address = self._serversocket.accept()
					connection.setblocking(0)
					self._epoll.register(connection.fileno(), select.EPOLLIN)
					self._connections[connection.fileno()] = connection
					self._requests[connection.fileno()] = b''
					self._responses[connection.fileno()] = b''
				elif event & select.EPOLLIN:
					client = self._connections[fileno]
					request = b''	
					request = b''
					try:
						while True:
							buffer_in = client.recv(4096)
							if not buffer_in or buffer_in == b'':
								break
							request += buffer_in
					except socket.error:
						pass
					self._epoll.modify(fileno, select.EPOLLOUT)
					request = self._requests[fileno] = TCPRequest(address, request) 
					response = self._responses[fileno] = TCPResponse()
					tcp_handler(request, response)
				elif event & select.EPOLLOUT:
					client = self._connections[fileno]
					response = self._responses[fileno]
					byteswritten = client.send(response.data)
					response.data = response.data[byteswritten:]
					if len(response.data) == 0:
						self._epoll.modify(fileno, select.EPOLLHUP)
						client.shutdown(socket.SHUT_RDWR)
				elif event & select.EPOLLHUP:
					self._epoll.unregister(fileno)
					self._connections[fileno].close()
					del self._connections[fileno]
					del self._requests[fileno]
					del self._responses[fileno]
	
	def finalize(self):
		self._epoll.unregister(self._serversocket.fileno())
		self._epoll.close()
		self._serversocket.close()
