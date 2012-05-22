#!/usr/bin/env python3

import sys, os
import unittest

sys.path.append(os.getcwd() + "/src")
sys.path.append(os.getcwd() + "/test")

TEST_MODULES = [
	'wsgi_test'
]

all_tests = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
	unittest.main()	
