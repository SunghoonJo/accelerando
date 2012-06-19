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
	def __init__(self, method, uri, version, headers, content_length, body = None):
		self.method = method
		self.uri = uri
		self.version = version
		self.headers = headers
		self.content_length = content_length
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

from accelerando.core import *
from accelerando.tcp import TCPProcessor

class HTTPProcessor(TCPProcessor):

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

	def route(self, uri):
		handler_name = self.application_context.handler_mappings[http_request.uri]
		handler = self.application_context.wsgi_handlers[handler_name]	
		handler(None, None)

	def handle_request(self):
		http_request = self._parse_http_request()
		headers = {
			b'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S EDT').encode('UTF-8'),
			b'Server': b'Accelerando',
			b'Content-Type': b'text/html; charset=UTF-8'
		}
		handler = self.route(http_request.uri)
		result = handler(env, start_response)
		try:
			for data in result:
				if data:
					write(data)
				if not headers_sent:
					write('')
		finally:
			if hasattr(result, 'close'):
				result.close()
	
		http_response = HTTPResponse(http_request.version, b'200 OK', headers, b'Success')
		
		return http_response.to_bytes()
			
