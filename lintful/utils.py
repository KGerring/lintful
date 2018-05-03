#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip




__all__ = ['clean_option_providers']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from startups.helpers.decorators import ExportsList, return_as
from lintful.base import get_linter
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


def clean_option_providers(linter):
	#OptionsManagerMixIn
	new_options_providers = sorted(set(linter.options_providers),
	                               key=lambda x: x.priority, reverse=True)
	
	setattr(linter, 'options_providers', new_options_providers)


@__all__.add
def meta_config(linter):
	"""
	Return the config as `optparse.Values` (linter.config) for all checkers
	:param linter:
	:return:
	
	>>> meta = meta_config(get_linter())
	>>> jobs = meta.jobs
	>>> jobs in list(range(1, 5))
	True
	
	"""
	from optparse import Values
	
	meta = Values(linter.config.__dict__)
	for checker in linter.prepare_checkers():
		meta.__dict__.update(checker.config.__dict__)
	
	return meta


@__all__.add
def enabled_messages(linter):
	"""
	
	:param linter:
	:return:
	
	>>> enabled = enabled_messages(get_linter())
	>>> 'fatal' in enabled
	True
	"""
	return set(filter(linter.is_message_enabled, linter.msgs_store._messages.copy()))


@__all__.add
def disabled_messages(linter):
	"""
	
	:param linter:
	:return:
	
	>>> disabled = disabled_messages(get_linter())
	>>> 'delslice-method' in disabled
	True
	"""
	
	from itertools import filterfalse
	return set(filterfalse(linter.is_message_enabled, linter.msgs_store._messages.copy()))


@__all__.add
def enabled_reports(linter):
	import itertools
	return [report for report in itertools.chain.from_iterable(
			linter._reports.values()) if linter.report_is_enabled(report[0])]


def disabled_reports(linter):
	import itertools
	
	return [report for report in itertools.chain.from_iterable(
			linter._reports.values()) if not linter.report_is_enabled(report[0])]


@__all__.add
def checker_messages(linter, enabled_only=False):
	"""
	
	:param linter:
	:param enabled_only:
	:return:
	
	>>> messages = checker_messages(get_linter())
	>>> 'master' in messages.keys()
	True
	
	"""
	from collections import OrderedDict
	
	results = OrderedDict()
	for checker_name in sorted(linter._checkers):
		checkerdict = OrderedDict()
		for mid in sorted(linter._checker_messages(checker_name)):
			if enabled_only and not linter.is_message_enabled(mid):
				pass
			else:
				checkerdict[mid] = linter._message_symbol(mid)
		results[checker_name] = checkerdict
	return results


#r'_.*|^ignored_|^unused_'
####L.config_parser.set('VARIABLES', 'ignored-argument-names', r'_.*|[a-zA-Z]|^ignored_|^unused_')
@__all__.add
def self_save_config_parser(linter):
	"""
	
	:param linter:
	:return:
	"""
	with open(linter.config_file, 'w') as fp:
		linter.cfgfile_parser.write(fp)
		print('Updated: {!r}'.format(linter.config_file), file = sys.stdout)




@__all__.add
def get_all_options(linter):
	"""
	Return all the options in all the providers for linter  _load_reporter_class
	
	#'lint'options_and_values,prepare_checkers,option_groups,load_defaults,et_checkers
	
	list(LL.options_by_section())[3][0]
	
	
	
	sorted(LL._all_options.values(), key = lambda x: x.priority, reverse = True)

	"""
	import optparse
	from addict import Dict
	providers = Dict()
	for provider in linter.options_providers:
		for opt, optdict in provider.options:
			action = optdict.get('action', None)
			if action != 'callback':
				if optdict is None:
					try:
						optdict = provider.get_option_def(opt)
						attrname = provider.option_attrname(opt)
						optdict['attrname'] = attrname[:]
						optdict['opt'] = opt[:]
						optdict['provider'] = provider.name.upper()
						providers[attrname] = optdict.copy()
					except optparse.OptionError:
						pass
				else:
					attrname = provider.option_attrname(opt)
					optdict['attrname'] = attrname[:]
					optdict['opt'] = opt[:]
					optdict['provider'] = provider.name.upper()
					providers[attrname] = optdict.copy()
	return providers




if __name__ == '__main__': print(__file__)