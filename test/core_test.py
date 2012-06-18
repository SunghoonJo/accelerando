import unittest
import collections
import sys, os, os.path
from accelerando.core import *

class CoreTest(unittest.TestCase):

	@classmethod
	def setUpClass(clazz):
		sys.path.append(os.getcwd())

	def test_load_application(self):
		application = load_application(os.getcwd() + '/application.py')
		self.assertNotEqual(application, None)
		self.assertTrue(isinstance(application, collections.Callable))
