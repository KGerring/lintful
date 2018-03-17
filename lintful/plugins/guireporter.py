#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = guireporter
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import linecache
import pylint.utils
import pylint.config
import pylint.lint

from pylint.reporters import BaseReporter
#from pylint.reporters.json import JSONReporter
#from pylint.reporters.ureports.text_writer import TextWriter

from lintful.plugins.base import Reporter, ReporterMessage





#return getline(abspath, line)[column:].strip()


#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__





if __name__ == '__main__': print(__file__)