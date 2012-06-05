class Cookie(object):
	pass

class Session(object):
	pass

class CookieSession(Session):
	pass

class ServerSession(Session):
	pass


from accelerando.handler import TCPHandler
class HTTPHandler(TCPHandler):

	def execute(self):
		pass
