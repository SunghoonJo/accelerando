
class TCPHandler(object):
	def __call___(self, socket, address):
		pass

class SimpleReactTCPHandler(TCPHandler):
	def __call__(self, socket, address):
		data = socket.recv(8192)
		print("address : ", address)
		print("data :")
		print(data)


from accelerando.handler.http import HTTPHandler
