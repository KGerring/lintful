#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = __init__.py
# author=KGerring
# date = 4/3/18
# from startups import *
"""

"""

from __future__ import absolute_import, unicode_literals # isort:skip
#__all__ = [] 
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from .checkers_patch import patch_checkers
from .messages_patch import patch_messages

def _patch_all():
	"""Execute all patches defined in this module."""
	from python_ta.patches import patch_checkers
	
	patch_checkers()
	patch_messages()
	#patch_type_inference_transform()
	#patch_messages()
	#patch_linter_transform()


#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__



if __name__ == '__main__': print(__file__)


