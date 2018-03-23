#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = base
# author= KGerring
# date = 3/23/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
from astroid import scoped_nodes
from pylint.checkers import BaseChecker
from . import utils
import astroid
import copy



__all__ = ['AstroidModuleFile', 'BaseRefactor', 'BaseRefactoringFile']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__



class BaseRefactor(BaseChecker):
	name = 'base'
	"""
	Base class for refactoring-options
	"""
	pass



class BaseRefactoringFile(object):
	def __init__(self, path, encoding='utf-8'):
		self.path = path
		self.encoding = encoding
	
	def __fspath__(self): return self.path
	
	def open(self):
		pass
	
	def close(self):
		pass



class AstroidModuleFile(astroid.scoped_nodes.Module):
	_ext = 'astroid'
	
	#def __new__(cls, linter):
	#	astroid_module = linter.get_ast(linter.current_file, linter.current_name)
	#	self = copy.copy(astroid_module)
	#	self.pure_python = False
	#	newfile = os.path.splitext(self.file)[0] + '.astroid'
	#	self.file = newfile[:]
	#	with self._get_stream() as reader:
	#		self.file_bytes = reader.read()
	#	#with open(self.file, 'wb') as writer:
	#	#	writer.write(self._get_stream().read())
	#	return self
	
	@classmethod
	def from_linter(cls, linter):
		linter = linter
		astroid_module = linter.get_ast(linter.current_file, linter.current_name)
		self = copy.copy(astroid_module)
		self.pure_python = False
		with self._get_stream() as reader:
			self.file_bytes = reader.read()
		newfile = os.path.splitext(self.file)[0] + '.astroid'
		self._old_file = self.file[:]
		self.file = newfile[:]
		return self



if __name__ == '__main__': print(__file__)