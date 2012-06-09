
class TCPRequest(object):
	def __init__(self, address, data):
		self.address = address
		self.data = data

class TCPResponse(object):
	def __init__(self):
		self.data = b''

class TCPServer(object):

	def __init__(self, hostname, port, backlog, dispatcher):
		self.dispatcher = dispatcher(hostname, port, backlog)
	
	def run(self, tcp_handler):
		if not self.dispatcher:
			raise Exception("Dispatcher cannot be None!")
		if not tcp_handler:
			raise Exception("TCPHandler cannot be None!")

		try:
			self.dispatcher.initialize()
			
			print("server initialize...")
			
			self.dispatcher.dispatch_and_handle(tcp_handler)
			
		finally:
			self.dispatcher.finalize()
			print("server finalize...")
