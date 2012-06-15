import unittest,os
from accelerando.package import *

class PackageTest(unittest.TestCase):

	def test_has_manifest(self):
		dirname = os.path.dirname(__file__)
		self.assertFalse(has_manifest(dirname + '/no_exist_manifest.py'))
		self.assertTrue(has_manifest(dirname + '/manifest.py'))

	def test_load_application_manifest(self):
		dirname = os.path.dirname(__file__)
		manifest = load_application_manifest(dirname + '/manifest.py')
		self.assertNotEqual(manifest, None)
		
	def test_manifest(self):
		manifest(
				name='Test Application'
		)

