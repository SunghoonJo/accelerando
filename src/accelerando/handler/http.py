class Cookie(object):
	pass

class Session(object):
	pass

class CookieSession(Session):
	pass

class ServerSession(Session):
	pass


from accelerando.handler import TCPHandler

class HTTPRequest(object):
	def __init__(self):
		pass
	
class HTTPResponse(object):
	def __init__(self):
		pass

class HTTPHandler(TCPHandler):
	def __call__(self, socket, address):
		request = HTTPRequest()
		response = HTTPResponse()
		socket.recv(1000)
