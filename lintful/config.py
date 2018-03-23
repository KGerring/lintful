#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = config
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from pylint.config import ConfigurationMixIn, OptionsManagerMixIn, Option
import configparser

PYLINT_CONFIG = os.environ.get('PYLINT_CONFIG', None)

_parser = configparser.ConfigParser(inline_comment_prefixes=('#', ';')) #TODO remove
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


@__all__.add
def find_lintfulrc():
	"""search the lintfulrc rc file and return its path if it find it, else None
	"""
	# is there a lintfulrc rc file in the current directory ?
	if os.path.exists('lintfulrc'):
		return os.path.abspath('lintfulrc')
	if os.path.exists('.lintfulrc'):
		return os.path.abspath('.lintfulrc')
	if os.path.isfile('__init__.py'):
		curdir = os.path.abspath(os.getcwd())
		while os.path.isfile(os.path.join(curdir, '__init__.py')):
			curdir = os.path.abspath(os.path.join(curdir, '..'))
			if os.path.isfile(os.path.join(curdir, 'lintfulrc')):
				return os.path.join(curdir, 'lintfulrc')
			if os.path.isfile(os.path.join(curdir, '.lintfulrc')):
				return os.path.join(curdir, '.lintfulrc')
	if 'LINTFULRC' in os.environ and os.path.exists(os.environ['LINTFULRC']):
		lintfulrc = os.environ['LINTFULRC']
	else:
		user_home = os.path.expanduser('~')
		if user_home == '~' or user_home == '/root':
			lintfulrc = '.lintfulrc'
		else:
			lintfulrc = os.path.join(user_home, '.lintfulrc')
			if not os.path.isfile(lintfulrc):
				lintfulrc = os.path.join(user_home, '.config', 'lintfulrc')
	if not os.path.isfile(lintfulrc):
		if os.path.isfile('/etc/lintfulrc'):
			lintfulrc = '/etc/lintfulrc'
		else:
			lintfulrc = None
	return lintfulrc







if __name__ == '__main__': print(__file__)