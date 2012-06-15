import unittest

import accelerando.processor.http
from accelerando.processor.http import HTTPRequestBuilder

class HTTPRequestBuilderTest(unittest.TestCase):

	def setUp(self):
		self.builder = HTTPRequestBuilder()

	def test_parse_segment(self):
		segment = b'GET / HTTP/1.1'
		self.builder.parse_segment(segment)
		self.assert_equals(b'GET', self.builder.method)
	
	def test_build(self):
		pass
