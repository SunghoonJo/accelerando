import os.path

def load_application(application_script_path):
	if os.path.exists(application_script_path):
		application_script = StringIO()
		with open(application_script_path) as f:
			application_script.write(fp.read())

		f.close()
		eval(application_script)
		return application
	else:
		raise Exception

