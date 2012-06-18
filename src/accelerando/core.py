import os.path

def load_application(application_manifest_name='manifest'):
	application_manifest = __import__(application_manifest_name)
	if application_manifest is not None:
		return application_manifest
	else:
		raise Exception
