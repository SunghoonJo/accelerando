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
	def __init__(self, method, uri, version, headers = {}, body = None):
		self.method = method
		self.uri = uri
		self.version = version
		self.headers = headers
		self.body = body

class HTTPResponse(object):
	def __init__(self, version, status_code, headers = {}, body = b''):
		self.version = version
		self.status_code = status_code
		self.headers = headers
		self.body = body
	
	def to_bytes(self):
		out = BytesIO() 
		
		out.write(b''.join([b'HTTP/', b'.'.join(map(bytes, self.version)), b' ', bytes(self.status_code), b'\r\n']))
		for header, value in self.headers.items():
			out.write(b''.join([header, b': ', value, b'\r\n']))
		out.write(b''.join([b'\r\n', self.body]))
		return out.getvalue()

INT_CR = int.from_bytes(b'\r', 'little')
INT_LF = int.from_bytes(b'\n', 'little')

class HTTPRequestBuilder(object):
	def __init__(self):
		self.segments = BytesIO()
		self.index = 0
		self.flag_header = True

		self.method = None 
		self.uri = None
		self.version = None
		self.url = None
		self.port = None
		self.headers = {}
		self.body = None

	def parse_segment(self, segment):
		self.segments.write(segment)
		segments_buffer = self.segments.getvalue()
		flag_parse = False
		end = 0
		len_segments = len(segments_buffer)
		for i in range(self.index, len_segments):
			if not self.method or not self.uri or not self.version:
				if i+1 < len_segments and segments_buffer[i] == INT_CR and segments_buffer[i+1] == INT_LF:
					end = i
					flag_parse = True
				if flag_parse and self.index < end:
					line = segments_buffer[self.index:end]
					self.index = end + 2
					elements = line.split()
					self.method = elements[0]
					self.uri = elements[1]
					self.version = elements[2]
					flag_parse = False
			elif self.flag_header:
				if i+1 < len_segments and segments_buffer[i] == INT_CR and segments_buffer[i+1] == INT_LF:	
					if i+3 < len_segments and segments_buffer[i+2] == INT_CR and segments_buffer[i+3] == INT_LF:	
						self.flag_header = False
					end = i
					flag_parse = True
				if flag_parse and self.index < end:
					line = segments_buffer[self.index:end]
					self.index = end + 2
					elements = line.split(b': ')
					self.headers[elements[0]] = elements[1]
					flag_parse = False
					if not flag_header:
						self.index += 2
			else:
				self.body = segments_buffer[self.index:len_segments]
				break
			

	def build(self):
		http_request = HTTPRequest(self.method, self.uri, self.version, self.headers, self.body)
		return http_request

from accelerando.tcp import TCPProcessor

class HTTPProcessor(TCPProcessor):

	def handle_request(self, http_request):
		print(http_request.method)
		print(http_request.uri)
		print(http_request.version)
		for header, value in http_request.headers.items():
			print(header, value)
		print(http_request.body)
		# file or wsgi handler will be here and process request
		headers = {
			b'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S EDT').encode('UTF-8'),
			b'Server': b'Accelerando',
			b'Content-Type': b'text/html; charset=UTF-8'
		}
		http_response = HTTPResponse(http_request.version, b'200 OK', headers, b'This is Response!')
		return http_response.to_bytes()
