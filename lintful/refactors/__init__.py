#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = __init__.py
# author=KGerring
# date = 3/16/18
# from startups import *
"""

"""

from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__
from astroid import scoped_nodes
from pylint.checkers import BaseChecker
from . import utils



@__all__.add
class BaseRefactor(BaseChecker):
	name = 'base'
	"""
	Base class for refactoring-options
	"""
	pass


@__all__.add
class BaseRefactoringFile(object):
	def __init__(self, path, encoding = 'utf-8'):
		self.path = path
		self.encoding = encoding
		
	def __fspath__(self): return self.path


	def open(self):
		pass
	
	def close(self):
		pass



#astroid.scoped_nodes.Module





if __name__ == '__main__': print(__file__)


