
def application(env, start_response):
	status = b'200 OK'
	response_headers = [(b'Content-type', b'text/html')]
	print('handler1')
	start_response(status, response_headers)
	return [b"Handler1\n"]
