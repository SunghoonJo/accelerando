from datetime import datetime
from io import BytesIO

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
	def __init__(self, version, status_code, headers = None, body = b''):
		self.version = version
		self.status_code = status_code
		if type(headers) == dict:
			self.headers = headers
		else:
			headers = {}
		self.body = body
	
	def to_bytes(self):
		out = BytesIO() 
		out.write(b'HTTP/')
		out.write(self.version)
		out.write(b' ')
		out.write(self.status_code)
		out.write(b'\r\n')
		for header, value in self.headers.items():
			out.write(header)
			out.write(b': ')
			out.write(value)
			out.write(b'\r\n')
		out.write(b'\r\n')
		out.write(self.body)
		return out.getvalue()

from accelerando.tcp import TCPProcessor

class HTTPProcessor(TCPProcessor):
	def initialize(self):
		self.request = HTTPRequest()
	
	def receive_request(self, buffer_in):
		# receive request and parse http request. HTTPRequest Object will be made
		pass

	def handle_request(self):
		# file or wsgi handler will be here and process request
		headers = {
			b'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S EDT').encode('UTF-8'),
			b'Server': b'Accelerando',
			b'Content-Type': b'text/html; charset=UTF-8'
		}
		response = HTTPResponse(b'1.0', b'200 OK', headers, b'This is Response!')
		return response.to_bytes()
