#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['token_column_distance', 'TokenWrapper']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__
import tokenize
from pylint.checkers.format import TokenWrapper, _column_distance as token_column_distance

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseTokenChecker





if __name__ == '__main__': print(__file__)