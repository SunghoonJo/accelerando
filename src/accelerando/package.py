import os.path
from io import StringIO

def has_manifest(manifest_filename):
	if os.path.exists(manifest_filename):
		return True
	else:
		return False

def load_application_manifest(manifest_filename='manifest.py'):
	if has_manifest(manifest_filename):
		manifest_io = StringIO()
		with open(manifest_filename) as fp:
			for line in iter(fp.readline, ''):
				manifest_io.write(line)
		
		manifest = eval(manifest_io.getvalue())
		manifest_io.close()
	else:
		raise Exception

def manifest(**attrs):
	raise Exception
