#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
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

from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

@__all__.add
def meta_config(linter):
	"""
	Return the config as `optparse.Values` (linter.config) for all checkers
	:param linter:
	:return:
	"""
	from optparse import Values
	
	meta = Values(linter.config.__dict__)
	for checker in linter.prepare_checkers():
		meta.__dict__.update(checker.config.__dict__)
	
	return meta




if __name__ == '__main__': print(__file__)