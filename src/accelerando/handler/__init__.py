
class TCPHandler(object):
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address

	def execute(self):
		pass

class SimpleReactTCPHandler(TCPHandler):
	def execute(self):
		print(self.address)

from accelerando.handler.http import HTTPHandler
