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
from . import serializers
from . import refactors


import setup_module
all_by_module = {
	'lintful.base': ['get_linter'],
	'lintful.config': ['find_lintfulrc', 'PYLINT_CONFIG'],
	'lintful.handlers': ['BaseHandler'],
	'lintful.plugins': [],
	'lintful.refactors': ['BaseRefactor', 'BaseRefactoringFile'],
	'lintful.refactors.utils': ['OPTIONS', 'get_import_names'],
	'lintful.serializers': ['ExternalDependenciesGraph', 'get_graphviz_source', 'make_tree_defs', 'run_dot', 'string_tree_defs'],
	'lintful.utils': ['meta_config'],
	'pylint.lint': ['PyLinter'],
}

old_module = sys.modules['lintful']
module = new_module = setup_module.module('lint_ful', all_by_module =all_by_module)


if __name__ == '__main__':
	print(__file__)