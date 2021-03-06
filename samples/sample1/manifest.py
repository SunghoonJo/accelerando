from accelerando.core import manifest
import handler1, handler2

APPLICATION_CONTEXT = manifest(
		hostname='211.189.127.88',
		title='Blog Application', 
		wsgi_handlers={
			'handler1': handler1.application,
			'handler2': handler2.application
		},
		handler_mappings={
			b'/': 'handler1',
			b'/handler2': 'handler2'
		}
)
