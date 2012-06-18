from io import BytesIO

class TCPProcessor(object):
	def __init__(self, address, application_context):
		self.address = address
		self.socketin = BytesIO()
		self.socketout = BytesIO()
		self.application_context = application_context

	def handle_request(self):
		pass

