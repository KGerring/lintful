#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename = importpy.linting.formatting
# author= KGerring
from __future__ import absolute_import, unicode_literals # isort:skip
#__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups import ExportsList
_all_ = []
__all__ = ExportsList(initlist=_all_[:], __file__=__file__)   # all-decorator: _all_

from . import base
from . import config
from . import plugins
from . import handlers
from . import interfaces
from . import patches
from . import serializers
from . import refactors
from . import reports
from . import utils

import setup_module

TODO = ["~/.cache", '~/.config', "startups.CACHE"]



#print('old path for {}'.format(__file__))
#print(__path__)
#print()
#import pkgutil
#__path__ = pkgutil.extend_path(__path__, __name__)
#print('new path for {}'.format(__file__))
#print(__path__)
#print()
#
#__path__.reverse()

def resolve(module_name, dotted_path):
	"""use instead of stuf.utils.lazyimport"""
	if module_name in sys.modules:
		mod = sys.modules[module_name]
	else:
		mod = __import__(module_name)
	if dotted_path is None:
		result = mod
	else:
		parts = dotted_path.split('.')
		result = getattr(mod, parts.pop(0))
		for p in parts:
			result = getattr(result, p)
	return result


all_by_module = {
	'lintful.base': set(['get_linter', '_do_load', 'LinterMixIn']),
	'lintful.config': {'find_lintfulrc', 'PYLINT_CONFIG'},
	'lintful.handlers': {'BaseHandler'},
	'lintful.config': {'OPTIONS'},
	
	'lintful.plugins.base': {'ColorReporter', 'Reporter', 'ReporterMessage'},
	'lintful.plugins.utils': {'Stats'},
	'lintful.refactors': {'BaseRefactor', 'BaseRefactoringFile'},
	'lintful.refactors.utils': {'get_import_names'},
	'lintful.serializers': {'ExternalDependenciesGraph', 'get_graphviz_source', 'make_tree_defs', 'run_dot', 'string_tree_defs'},
	
	
	'lintful.utils': set(['meta_config']),
	'pylint.lint': set(['PyLinter']),
	'importpy.linting.formatting': set(['MessagesSorter']),
}

for k,v in all_by_module.items():
	v = set(v)

old_module = sys.modules['lintful']
module = new_module = setup_module.module('lint_ful', all_by_module =all_by_module)


if __name__ == '__main__':
	print(__file__)