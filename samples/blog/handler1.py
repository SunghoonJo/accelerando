
def application(env, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	print('handler1')
#start_response(status, response_headers)
	return [b"Hello world!\n"]
