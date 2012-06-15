
from accelerando.tcp import TCPServer
from accelerando.processor.http import HTTPProcessor
from accelerando.dispatcher import EPollDispatcher

class StandaloneHTTPInstance(object):
	def __init__(self, hostname, port,listen=100,dispatcher=EPollDispatcher,processor=HTTPProcessor):
		self.hostname = hostname
		self.port = port
		self.listen = listen
		self.dispatcher = dispatcher
		self.processor = processor

	def run_forever(self):
		server = TCPServer(self.hostname, self.port, self.listen, self.dispatcher)
		server.run(self.processor)
