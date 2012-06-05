#!/usr/bin/env python3

import unittest
import accelerando.wsgi

class WSGIHandlerTest(unittest.TestCase):

	def setUp(self):
		pass

	def test_handle(self):
		def application(env, start_response):
			pass

		WSGIHandler(application).handle()	
