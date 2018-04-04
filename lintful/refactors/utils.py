#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip




__all__ = ['get_dots_on_path', 'expand_files']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from startups.helpers.decorators import ExportsList
from importpy.refactoring.misc import get_dots_on_path
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

#lintful.config.OPTIONS
#lintful.__loader__.get_data('options.yaml')


@__all__.add
def get_import_names(node):
	"""
	Return the import-names for an astroid-node
	:param node:
	:return:
	"""
	from pylint.checkers.variables import NamesConsumer
	to_consume = NamesConsumer(node, 'module')
	not_consumed = to_consume.to_consume
	local_names = pylint.checkers.variables._fix_dot_imports(not_consumed)
	return local_names


def expand_files(files, linter):
	from pylint.utils import expand_modules
	if not linter:
		return expand_modules(files, [], [])
	else:
		return expand_modules(files, linter.config.black_list, linter.config.black_list_re)
		



if __name__ == '__main__': print(__file__)