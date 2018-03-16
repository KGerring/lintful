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

from importpy.refactoring._pylint import get_linter_rcfile as get_linter

TODO = ['PyLinter.set_current_module',
        'PyLinter.prepare_checkers',
        'open',
        'load_plugin_modules',
        'load_default_plugins',
        'get_ast',
        'generate_reports',
        'check_astroid_module',
        'self.reporter.on_set_current_module(modname, filepath)']






if __name__ == '__main__': print(__file__)