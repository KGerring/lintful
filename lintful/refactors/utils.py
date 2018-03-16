#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip




__all__ = ['OPTIONS']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

OPTIONS = (
	('allow-local-reimport',
	 {'default': True,
	  'help': 'Allow a reimport of something within a function or class (to allow moving)',
	  'metavar': '<y_or_n>', 'type': 'yn'}),

)


@__all__.add
def get_import_names(node):
	from pylint.checkers.variables import NamesConsumer
	to_consume = NamesConsumer(node, 'module')
	not_consumed = to_consume.to_consume
	local_names = pylint.checkers.variables._fix_dot_imports(not_consumed)
	return local_names







if __name__ == '__main__': print(__file__)