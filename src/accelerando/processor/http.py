class Cookie(object):
	pass

class Session(object):
	pass

class CookieSession(Session):
	pass

class ServerSession(Session):
	pass

class HTTPRequest(object):
	def __init__(self):
		pass
	
class HTTPResponse(object):
	def __init__(self):
		pass

from accelerando.tcp import TCPProcessor

class HTTPProcessor(TCPProcessor):
	def initialize(self):
		pass
	
	def receive_request(self, buffer_in):
		pass

	def handle_request(self):
		pass
