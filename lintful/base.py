#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = base
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = ['get_linter']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

import pylint.lint
from pylint.utils import _splitstrip, _unquote, _MsgBase

TODO = ['PyLinter.set_current_module',
        'PyLinter.prepare_checkers',
        'open',
        'load_plugin_modules',
        'load_default_plugins',
        'get_ast',
        'generate_reports',
        'check_astroid_module',
        'self.reporter.on_set_current_module(modname, filepath)']

RCFILE = os.environ.get("PYLINTRC")


def _do_load(linter):
	"""
	Workaround if the patched pylint.lint doesn't exist (i.e No PyLinterMixIn class).
	:param linter:
	:return:
	"""
	from pylint import config
	from pylint.utils import _splitstrip
	linter.load_defaults()
	try:
		linter.load_default_plugins()
	except Exception:
		pass
	config_file = getattr(linter, 'config_file', config.PYLINTRC)
	linter.read_config_file(config_file)
	
	if linter.cfgfile_parser.has_option('MASTER', 'load-plugins'):
		plugins = _splitstrip(linter.cfgfile_parser.get('MASTER', 'load-plugins'))
		linter.load_plugin_modules(plugins)
	
	linter.load_config_file()
	print('External "_do_load" complete!', file = sys.stderr)


def get_linter(rcfile = RCFILE):
	from pylint.lint import PyLinter
	linter = PyLinter(pylintrc= rcfile)
	if hasattr(linter, '_do_load'):
		linter._do_load()
	else:
		_do_load(linter)
		
	return linter
	


if __name__ == '__main__': print(__file__)