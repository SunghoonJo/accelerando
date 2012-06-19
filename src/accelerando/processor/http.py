import sys, os
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
	def __init__(self, method, uri, version, headers, content_length, body=None):
		self.method = method
		self.uri = uri
		self.version = version
		self.headers = headers
		self.content_length = content_length
		self.body = body

class HTTPResponse(object):
	def __init__(self, version, status=None, headers=None, body=BytesIO()):
		self.version = version
		self.status= status
		self.headers = headers
		self.body = body
	
	def to_bytes(self):
		out = BytesIO() 
		out.write(b''.join([b'HTTP/', self.version, b' ', self.status, b'\r\n']))
		for header, value in self.headers.items():
			out.write(b''.join([header, b': ', value, b'\r\n']))
		out.write(b''.join([b'\r\n', self.body.getvalue()]))
		return out.getvalue()

from accelerando.core import *
from accelerando.tcp import TCPProcessor

class HTTPProcessor(TCPProcessor):

	def __init__(self, address, application_context):
		super().__init__(address, application_context)

	def _parse_http_request(self):
		request_bytes = self.socketin.getvalue()
		len_bytes = len(request_bytes)
		header_start = 0
		header_end = 0;
		body_start = 0;
		status_line_found = False
		for i in range(0, len_bytes-3):
			if not status_line_found:
				if b'\r\n' == request_bytes[i:i+2]:
					header_start = i+2
					status_line_found = True
			elif b'\r\n\r\n' == request_bytes[i:i+4]:
				header_end = i
				body_start = i+4
				break;

		status_line = request_bytes[0:header_start-2]
		header_bytes = request_bytes[header_start:header_end]
		body_bytes = request_bytes[body_start:len_bytes]

		method, uri, version = None, None, None
		for value in status_line.split(b' '):
			if not method:
				method = value
			elif not uri:
				uri = value
			else:
				version = value.split(b'/')[1]

		headers = {}
		content_length = 0
		for header_token in header_bytes.split(b'\r\n'):
			header_name, header_value = header_token.split(b': ')
			headers[header_name] = header_value
			if header_name == b'Content Length':
				content_length = int(header_value)

		return HTTPRequest(method, uri, version, headers, content_length, body_bytes)

	def _route(self, uri):
		if self.application_context.handler_mappings.get(uri):
			handler_name = self.application_context.handler_mappings[uri]
			if self.application_context.wsgi_handlers.get(handler_name):
				handler = self.application_context.wsgi_handlers[handler_name]	
				if handler:
					return handler
		
		raise Exception("NO HANDLER FOUND")
	
	def _write(self, data):
		assert type(data) is bytes
		self._http_response.body.write(data)

	def _start_response(self, status, headers, exc_info=None):
		assert self._http_response is not None
		if exc_info:
			try:
				#below codes are not valid
				if self.headers_sent:
					raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
			finally:
					exc_info = None
		elif self._http_response.headers is not None:
			 raise AssertionError("Headers already set!")

		self._http_response.status = status
		if self._http_response.headers is None:
			self._initialize_headers()

		for t in headers:
			self._http_response.headers[t[0]] = t[1]
		
		return self._write

	def _initialize_headers(self):
		assert self._http_response.headers is None
		self._http_response.headers = {}
		self._http_response.headers[b'Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S EDT').encode('UTF-8')
		self._http_response.headers[b'Server'] = b'Accelerando'

	def _initialize_environment(self, http_request):
		env = {}
		env['REQUEST_METHOD'] = http_request.method
		if self.application_context.handler_mappings.get(http_request.uri):
			env['SCRIPT_NAME'] = self.application_context.handler_mappings[http_request.uri]
		env['PATH_INFO'] = ''
		env['QUERY_STRING'] = ''
		if http_request.headers.get(b'Content-Type'):
			env['CONTENT_TYPE'] = http_request.headers[b'Content-Type']
		if http_request.headers.get(b'Content-Length'):
			env['CONTENT_LENGTH'] = http_request.headers[b'Content-Length']
		env['SERVER_NAME'] = ''
		env['SERVER_PORT'] = ''
#another http headers are here
		return env

	def handle_request(self):
		http_request = self._parse_http_request()
		env = self._initialize_environment(http_request)
		handler = self._route(http_request.uri)
		
		self._http_response = HTTPResponse(http_request.version)
		result = handler(env, self._start_response)
		try:
			for data in result:
				if data:
					self._write(data)
		finally:
			if hasattr(result, 'close'):
				result.close()
			
		return self._http_response.to_bytes()
			
