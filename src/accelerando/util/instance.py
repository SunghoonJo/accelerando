
import os

from accelerando.core import *

class StandaloneHTTPInstance(object):

	def __init__(self, application_context):
		self.application_context = application_context
		
	def run_forever(self):
		APPLICATION_CONTEXT = self.application_context
		HOSTNAME = APPLICATION_CONTEXT.hostname
		PORT = APPLICATION_CONTEXT.port
		BACKLOG = APPLICATION_CONTEXT.backlog
		
		DISPATCHER_CLASS = APPLICATION_CONTEXT.dispatcher_class
		TCP_PROCESSOR_CLASS = APPLICATION_CONTEXT.tcp_processor_class
		
		assert(DISPATCHER_CLASS is not None)
		assert(TCP_PROCESSOR_CLASS is not None)

		dispatcher = DISPATCHER_CLASS(HOSTNAME, PORT, BACKLOG, APPLICATION_CONTEXT)
		
		dispatcher.initialize()
		
		print("server initialize...")
		try:	
			dispatcher.dispatch_and_handle(TCP_PROCESSOR_CLASS)
		finally:
			dispatcher.finalize()
			print("server finalize...")
