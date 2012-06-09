
class TCPHandler(object):
	def __call___(self, socket, address):
		pass

class SimpleReactTCPHandler(TCPHandler):
	def __call__(self, request):
		print(request)


from accelerando.handler.http import HTTPHandler
