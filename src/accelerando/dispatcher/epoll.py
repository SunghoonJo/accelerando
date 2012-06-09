import socket, select

from accelerando.dispatcher import Dispatcher

class EPollDispatcher(Dispatcher):

	def __call__(self, hostname, port, backlog, tcp_handler_class):
		if not tcp_handler_class:
			raise Exception

		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind((hostname, port))
		serversocket.listen(backlog)
		serversocket.setblocking(0)

		epoll = select.epoll()
		epoll.register(serversocket.fileno(), select.EPOLLIN)
		try:
			connections = {}; responses = {}
			while True:
				events = epoll.poll(1)
				for fileno, event in events:
					if fileno == serversocket.fileno():
						connection, address = serversocket.accept()
						connection.setblocking(0)
						epoll.register(connection.fileno(), select.EPOLLIN)
						connections[connection.fileno()] = connection
					elif event & select.EPOLLIN:
						client = connections[fileno]
						request = b''	
						try:
							while True:
								buffer_in = client.recv(4096)
								if not buffer_in or buffer_in == b'':
									break
								request += buffer_in
						except socket.error:
							pass
						
						epoll.modify(fileno, select.EPOLLOUT)
						print(address, " connected to server")

						tcp_handler = tcp_handler_class()
						responses[client.fileno()] = tcp_handler(request)
					elif event & select.EPOLLOUT:
						client = connections[fileno]
						byteswritten = client.send(responses[fileno])
						responses[fileno] = responses[fileno][byteswritten:]
						if len(responses[fileno]) == 0:
							epoll.modify(fileno, select.EPOLLHUP)
							client.shutdown(socket.SHUT_RDWR)
					elif event & select.EPOLLHUP:
						epoll.unregister(fileno)
						connections[fileno].close()
						del connections[fileno]
						print(client, " epoll hup")
		finally:
			epoll.unregister(serversocket.fileno())
			epoll.close()
			serversocket.close()

		return
