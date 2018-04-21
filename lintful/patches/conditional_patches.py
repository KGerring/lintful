#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = conditional_patches
# author= KGerring
# date = 4/4/18
# from startups import *
""" 


"""
from __future__ import absolute_import, unicode_literals # isort:skip
from lintful.config import resolve
try:
	from toolz import curry as partial  #toolz not found!
except Exception:
	from functools import partial


__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import itertools
#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

def get_stats_file_template_mapping(persistent_amt = 0):
	"""
	
	:param persistent_amt: A `lintful.config.Lint.config.persistent_amt` or PyLinter.config.persistent_amt;
		default is 0 (which has recurs = 1; so like default behavior)
	:return: A dict mapping recurs (1-indexed) to the filename-template with '{base}' as a format imput.
	
	>>> default_mapping = get_stats_file_template_mapping()
	>>> 1 in default_mapping
	True
	>>> len(default_mapping) == 1
	True
	>>> os.path.basename(default_mapping[1]) == '{base}1.stats'
	True
	>>> test_mapping = get_stats_file_template_mapping(4)
	>>> isinstance(test_mapping, dict)
	True
	>>> len(test_mapping) == max(test_mapping) == 5
	>>> '{base}'+str(3) in test_mapping[3]
	True
	
	"""
	if 'PYLINTHOME' in os.environ:
		PYLINT_HOME = os.environ.get('PYLINTHOME', None)
	if PYLINT_HOME is None:
		try:
			PYLINT_HOME = resolve('pylint.config', 'PYLINT_HOME')
		except Exception:
			PYLINT_HOME = os.path.join( os.path.expanduser('~'), '.pylint')
	else:
		PYLINT_HOME = os.path.join(os.path.expanduser('~'), '.pylint')
	if not os.path.exists(PYLINT_HOME):
		os.mkdir(PYLINT_HOME)
	base_recurs = 1
	max_recurs = base_recurs + persistent_amt
	#PYLINT_HOME = pylint.config.PYLINT_HOME
	TEMPLATES = dict()
	for i in range(base_recurs, max_recurs+1):
		tname = os.path.join(PYLINT_HOME, "%s%s%s" % ("{base}", i, '.stats'))
		TEMPLATES[i] = tname
	return TEMPLATES
		
	#os.path.join(pylint.config.PYLINT_HOME, "%s%s%s" % ("{base_name}", "{recurs}", '.stats'))
	#pylint.config._get_pdata_path (base_name, recurs = 1)

def resolve_PYLINT_HOME(): pass

def _overload_get_pdata_path():                 # TODO MonkeyPatch with setattr?        #persistent_amt?
	# TODO PROBLEM: doesn't automatically work with load/save results. #XXX #FIXME
	"""
	Reset `_get_pdata_path` for pylint.config to have recurs as a keyword-default argument with default = 1
		The function can be re-bound with the `recurs = new_limit` (type: int); or `recurs` can be passed
		as a keyword-argument. Used with `pylint.config.load_results` and `pylint.config.save_results`
		to allow for a different base-name integer-value (so 'base_name1.stats', 'base_name2.stats').
		Requires that the option `persistent_amt` is set to a non-negative integer OR it is defaulted. ??
	:return:  The curried-function with a partial-application of arguments, but with a cleaner-signature, etc.
	Uses `toolz.curry`
	"""
	old_get_pdata_path = resolve('pylint.config', '_get_pdata_path')
	_get_pdata_path_with_recurs_as_default = partial(old_get_pdata_path, recurs = 1)
	pylint_config_module = resolve('pylint', 'config')                  #????
	setattr(pylint.config, '_get_pdata_path', _get_pdata_path_with_recurs_as_default)
	####### if hasattr(_get_pdata_path_with_recurs_as_default, '__name__')     #TODO run assertion_tests
	# assert _get_pdata_path_with_recurs_as_default.func == old_get_pdata_path
	# assert newfunc.__qualname__ == old_get_pdata_path.__qualname__
	# newfunc.__signature__._parameters['recurs'].kind == inspect.Parameter.KEYWORD_ONLY
	# newfunc.__module__ == old_get_pdata_path.__module__
	

def _overload_load_results():
	"""load from largest to smallest end at 1 or return {}"""
	def _new_load_results(base):
		import pickle
		import pylint.config
		persistence_max = persistent_amt + 1
		persistence_min = 1
		result = {}
		while persistence_max > persistence_min:
			data_file = _get_pdata_path(base, persistence_max)
			if os.path.exists(data_file):
				try:
					with open(data_file, _PICK_LOAD) as stream:
						result =  pickle.load(stream)
						print('loading file from {}'.format(data_file))
				except Exception: # pylint: disable=broad-except
					continue
			persistence_max -= 1
		return result
			
def _overload_save_results():
	"""Try to save to higher if file already exists, unless max is reached, then to max, or default"""
	
	def _new_save_results(results, base):
		persistence_min = 1
		persistence_max = persistent_amt + 1

		while persistence_min < persistence_max:
			data_file = _get_pdata_path(base, persistence_min)
			if not os.path.exists(data_file):
				pass


	def save_results(results, base):
		if not os.path.exists(PYLINT_HOME):
			try:
				os.mkdir(PYLINT_HOME)
			except OSError:
				print('Unable to create directory %s' % PYLINT_HOME, file=sys.stderr)       #TODO
		data_file = _get_pdata_path(base, 1)                #######         persistent-amt overwrite with default recurs value???
		try:
			with open(data_file, _PICK_DUMP) as stream:
				pickle.dump(results, stream)
		except (IOError, OSError) as ex:
			print('Unable to create file %s: %s' % (data_file, ex), file=sys.stderr)


if __name__ == '__main__': print(__file__)