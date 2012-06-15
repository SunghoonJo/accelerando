#!/usr/bin/env python3

class WSGIHandler(object):

	def _create_environments(self):
		env = {k: unicode_to_wsgi(v) for k, v in os.environ.items()}
		env['wsgi.input'] = sys.stdin.buffer
		env['wsgi.errors'] = sys.stderr
		env['wsgi.version'] = (1, 1)
		env['wsgi.multithread'] = False
		env['wsgi.multiprocess'] = True
		env['wsgi.run_once'] = True
		if env.get('HTTPS', 'off') in ('on', '1'):
			env['wsgi.url_scheme'] = 'https'
		else:
			env['wsgi.url_scheme'] = 'http'

		return env

	def handle(self, application):
		env = self._create_environments()

		headers_set = []
		headers_sent = []

		def write(data):
			out = sys.stdout.buffer
			
			if not headers_set:
				raise AssertionError("write() before start_response()")
			elif not headers_sent:
				status, response_headers = headers_sent[:] = headers_set
				out.write(wsgi_to_bytes('Status: %s\r\n' % status))
				for header in response_headers:
					out.write(wsgi_to_bytes('%s: %s\r\n' % header))
				out.write(wsgi_to_bytes('\r\n'))

			out.write(data)
			out.flush()

		def start_response(status, response_headers, exc_info=None):
			if exc_info:
				try:
					if headers_sent:
						raise exc_info[1].with_traceback(exc_info[2])
				finally:
					exc_info=None
			elif headers_sent:
				raise AssertionError("Headers already set!")
			headers_set[:] = [status, response_headers]
		# WSGI Application will be started from here
		result = application(env, start_response)
		try:
			for data in result:
				if data:
					write(data)
				if not headers_sent:
					write('')
		finally:
			if hasattr(result, 'close'):
					result.close()

