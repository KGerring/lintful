#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = test_pylinter
# author= KGerring
# date = 3/24/18
"""

"""
import os
import sys
import unittest
import pylint.lint
from pylint.lint import PyLinter, PyLinterMixIn
PYLINTRC = os.environ.get('PYLINTRC')

class LintfulPyLinterTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.linter_class = PyLinter
		cls.mixin = PyLinter.__bases__[1]
		cls.mixin_name = PyLinter.__bases__[1].__name__
		linter = PyLinter()
		linter._do_load()
		cls.linter = linter
		
	
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	@classmethod
	def tearDownClass(cls):
		cls.linter.reset_parsers()
		print('parsers have been cleared/reset for linter!!', file=sys.stderr)


class TestLintfulPyLinterMixIn(LintfulPyLinterTestCase):
	
	def test_bases(self):
		basenames = [base.__name__ for base in self.linter_class.__bases__]
		self.assertIn(self.mixin_name, basenames, '{} not in base-class'.format(self.mixin_name))
		
	def test_overrides_add_message(self):
		funcname = self.linter.add_message.__func__.__qualname__
		self.assertTrue(funcname.startswith(self.mixin_name), 'add_message not coming from mixin-class')
		self.assertEqual(self.linter.add_message.__self__, self.linter, "add_message doesn't have PyLinter as __self__")
		
	def test_do_load(self):
		self.assertTrue(hasattr(self.mixin, '_do_load'))
		self.assertTrue(hasattr(self.linter, '_do_load'), 'PyLinter doesnt have _do_load')
		
		preloaded = PyLinter()
		self.assertFalse(preloaded.config.reports)
		self.assertLessEqual(len(preloaded.cfgfile_parser._sections), 5, 'cfgfile_parser already loaded')
		self.assertEqual(len(preloaded._dynamic_plugins), 0)
		
		preloaded._do_load()
		self.assertTrue(preloaded.config.reports, '"reports" option for PyLinter.config not modified from default')
		self.assertGreaterEqual(len(preloaded.cfgfile_parser._sections), 5)
		self.assertGreater(len(preloaded._dynamic_plugins), 0)

class TestRun(LintfulPyLinterTestCase):
	"""
	# TODO
	"""
	



if __name__ == '__main__':
	unittest.main(verbosity=3)