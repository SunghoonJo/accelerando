import os.path
import sys, os

from accelerando.dispatcher.epoll import EPollDispatcher
from accelerando.processor.http import HTTPProcessor

class ApplicationContext(object):
	def __init__(self, context_variables):
		self.title = context_variables['title']
		self.hostname = context_variables['hostname']
		self.port = context_variables['port']
		self.backlog = context_variables['backlog']
		self.dispatcher_class = context_variables['dispatcher_class']
		self.tcp_processor_class = context_variables['tcp_processor_class']
		self.wsgi_handlers = context_variables['wsgi_handlers']
		self.handler_mappings = context_variables['handler_mappings']

def manifest(**kargs):
	if kargs.get('hostname') is None:
		kargs['hostname'] = 'localhost'
	if kargs.get('port') is None:
		kargs['port'] = 4000
	if kargs.get('backlog') is None:
		kargs['backlog'] = 100
	if kargs.get('dispatcher_class') is None:
		kargs['dispatcher_class'] = EPollDispatcher
	if kargs.get('tcp_processor_class') is None:
		kargs['tcp_processor_class'] = HTTPProcessor
	return ApplicationContext(kargs)

def load_application(manifest_filename = 'manifest.py'):
	manifest_path = os.getcwd() + '/' + manifest_filename
	if os.path.exists(manifest_path):
		sys.path.append(os.getcwd())
		application_module = __import__('manifest');

		application_context = application_module.APPLICATION_CONTEXT
		return application_context
	else:
		raise Exception

