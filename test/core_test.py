import unittest
import collections
import sys, os, os.path

from accelerando.core import *

class CoreTest(unittest.TestCase):
	@classmethod
	def setUpClass(clazz):
		sys.path.append(os.getcwd())

	def test_load_application(self):
		sys.path.append(os.path.dirname(__file__))
		application = load_application()
		self.assertNotEqual(application, None)
