#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = config
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['OPTION_INFO', 'OPTIONS', 'PYLINT_CONFIG','PYLINTHOME', "Lint", 'resolve']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import yaml
from addict import Dict
from pylint.config import ConfigurationMixIn, OptionsManagerMixIn, Option, VALIDATORS
import configparser
import logilab.common.configuration as configuration
from logilab.common.decorators import monkeypatch
from pylint.checkers import BaseChecker, BaseTokenChecker
from python_ta.reporters.plain_reporter import ERROR_CHECKS
from pylint.reporters.ureports.nodes import Section, Table, EvaluationSection
from pathlib import Path
#from _pytest import monkeypatch as patch

from startups.helpers.decorators import ExportsList

__all__ = ExportsList(initlist=__all__, __file__=__file__) # all-decorator: __all__

PYLINT_CONFIG = os.environ.get('PYLINT_CONFIG', None)
PYLINTHOME = os.environ.get('PYLINTHOME', None)
PYLINTRC = os.environ.get('PYLINTRC', None)

def make_path():
	results = Dict()
	for path in Path(PYLINT_CONFIG).iterdir():
		results[path.stem] = str(path)
	return results

PYLINTPATH = make_path()



#'persistent' = True
#'score' = True
#'load_plugins'


#'enable'
#'black_list_re'


"""


LL.__dict__.get('_dynamic_plugins')
'_mygroups'
'_all_options'
'options_providers'
'_optik_option_attrs'
 'config_file',
 'cfgfile_parser',
 'cmdline_parser'
  '_external_opts',
 'options',
 'option_groups'
 'reporter',
 '_reporter_name',
 '_reporters',
 '_checkers'
 
 _msgs_state
 
 
"""


#config.save_results(self.stats, self.file_state.base_name)


#os.environ,'PYLINTHOME,PYLINTRC,PYLINT_CONFIG'



OPTION_INFO = Dict(dict(
		ACTIONS=Option.ACTIONS,
		STORE_ACTIONS=Option.STORE_ACTIONS,
		TYPES=Option.TYPES,
		ATTRS=Option.ATTRS,
		ATTRIBUTES=Option.ATTRS,
		VALIDATORS =VALIDATORS))


#from logilab.common.deprecation import class_moved


class LintOption(Option):
	TYPE_CHECKER = Option.TYPE_CHECKER
	TYPE_CHECKER['file'] = configuration.file_validator
	TYPES = Option.TYPES
	TYPES += ('file',)


OPTIONS = (
	('allow-local-reimport',
	 {'default': True,
	  'help': 'Allow a reimport of something within a function or class (to allow moving)',
	  'metavar': '<y_or_n>',
	  #'level': 1,
	  'type': 'yn'}),
	('persistent-amount',
	 {'default': 0,
	  'help': 'Number of backlogs of saved-stats',
	  'metavar': '<persistent-amt>',
	  'type': 'int'}),
	('prefix-import-graph',
	 {'default': True,
	  'help': "Should the imports.dot names be prefixed with the module base-name?",
	  'metavar': '<y_or_n>',
	  'type': 'yn',
	  }),
	('group-wildcard-imports',
	 {'default': True,
	  'help': 'group wildcard imports according to module',
	  'metavar': '<y_or_n>',
	  'type': 'yn'}),
	('message-type', dict(type = 'choice', choices = ('', 'yaml', 'json', 'csv'),
	                      default = 'json', help = 'Print message to console in this form')),
	('fix-different-reimport', dict(type = 'yn', default = True, metavar ='<y_or_n>',
	                                help="Fix import names for when multiple objects are imported with the same name from different modules")),
	
	)





def resolve(module_name, dotted_path):
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


def _all_by_module():
	items = Dict()
	ABM ={
		
		'logilab.common.ureports.nodes': ['Link', 'List', 'Image', 'Span'],
		'logilab.common.ureports.html_writer': ['HTMLWriter'],
		'logilab.common.ureports': ['BaseWriter'],
		'logilab.common.umessage': ['UMessage'],
		'logilab.common.tasksqueue': ['Task', 'PrioritizedTasksQueue'],
		'logilab.common.deprecation': ['deprecated', 'moved', 'class_renamed',
		                               'class_moved', 'class_deprecated', '_defaultdeprecator',
		                               'DeprecationManager', 'DeprecationWrapper'],
		
		'logilab.common.decorators': ['monkeypatch', ],
		'logilab.common.configuration': ['merge_options', 'file_validator',
		                                 'VALIDATORS', 'OptionsManager2ConfigurationAdapter', 'Method', #'INPUT_FUNCTIONS',
		                                 'ConfigurationMixIn',
		                                 'Configuration']
	}
	from stuf.utils import lazyimport
	for module, values in ABM.items():
		for value in values:
			try:
				a = resolve(module, value)
				items[value] = a
			except BaseException:
				pass
	return items

def make_option(optstr, _type=None, default=None, _help=None,
                metavar=None, short_opt = False, **kwargs):
	"""
	
	:param optstr:
	:param type:
	:param default:
	:param help:
	:param metavar:
	:param short_opt:
	:param kwargs:
	:return:
	"""
	if not _help:
		_help = 'Help for {}'.format(optstr)
		
	d = dict(default = default, metavar = metavar, help = _help, type = _type)
	kwds = kwargs.copy()
	d.update(kwds)
	
	
	if short_opt is True:
		d['short'] = optstr[0]
	elif isinstance(short_opt, str):
		d['short'] = short_opt[0][:]
	
	if not _type and default:
		if default in (True, False):
			_type = 'yn'
		elif isinstance(default, int):
			_type = 'int'
		elif isinstance(default, str) and ',' in default:
			_type = 'csv'
		else:
			_type = 'string'
		d['type'] = _type
	
	if _type == 'yn' and not metavar:
		d['metavar'] = '<y_or_n>'
		
	
	return (optstr, d)
			
			
		
#REPORTS,output-format,Reporter
#REPORTS,reports,yes
#load-plugins,persistent = yes;ignore-patterns,ignore

class LintParser(configparser.ConfigParser):
	_file = None
	
	def __init__(self, *args, **kwargs):
		self._file = kwargs.pop('file', self._file)
		super(LintParser, self).__init__(*args, **kwargs)
		self.inline_comment_prefixes = ('#', ';')
		
		if self._file and os.path.exists(self._file):
			self.read([self._file])
			
	def write_file(self):
		assert self._file, 'file doesnt exist!'
		with open(self._file, 'w') as writer:
			self.write(writer)
		return self._file
	
	
	def read_file(self, file):
		with open(file) as reader:
			pass
			
	
	
	
	@classmethod
	def from_file(cls, filename):
		klass = cls()
		if os.path.exists(filename):
			klass.read([filename])
			klass._file = filename[:]
		return klass
		

### TODO msg_template ='{symbol}: {msg} ({fullname})|{path}:{line}:{column}'

	

class Lint(BaseChecker):
	name = 'lint'
	priority = 0
	options = OPTIONS
	plugins = []
	rcfile = []#'docstyle'
	#level = 0
	option_groups = (('External', "Options External to pylint"),)
	reports =[]# [('RP6201', 'Evaluation', Lint.evaluation_callback)]
	EXTENSIONS = [#'pylint.extensions.check_elif.ElseifUsedChecker',
	              'pylint.extensions.docstyle.DocStringStyleChecker',
	              #'pylint.extensions.redefined_variable_type.MultipleTypesChecker',
	             # 'pylint.extensions.comparetozero.CompareToZeroChecker',
	             # 'pylint.extensions.overlapping_exceptions.OverlappingExceptionsChecker',
	             # 'pylint.extensions.emptystring.CompareToEmptyStringChecker',
	             # 'pylint.extensions.bad_builtin.BadBuiltinChecker',
		
		
	              'pylint.extensions.docparams.DocstringParameterChecker',
	              'pylint.extensions.mccabe.McCabeMethodChecker']
	
	to_enable = ('multiple-constructor-doc', 'missing-param-doc', 'too-complex')
	
	FIXES = ('bad-docstring-quotes')
	
	PLUGIN_MODULES = ('lintful.plugins.base',
	                  'lintful.config',
	                  'pylint.extensions.docparams',
	                  'pylint.extensions.docstyle',
	                  'pylint.extensions.mccabe',
	                 )
	"""
	'LINT',
 'External',
 'lintful',
 'PARAMETER_DOCUMENTATION']
	
	"""

	def __init__(self, linter = None):
		super().__init__(linter)
		self.append_reports()
		
	
	def _open(self):
		"""called before visiting project (i.e set of modules)"""
		self.open()
	
	def evaluation_callback(self, sect, stats, previous_stats):
		note, pnote, dnote = None, None, None
		#if not self.linter.config.evaluation:
		if self.linter and self.linter.config.evaluation:
			evaluation = self.linter.config.evaluation
		else:
			evaluation = '10.0 - ((float(5 * error + warning + refactor + convention) / statement) * 10)'
		
		if stats['statement'] == 0:
			return
		if 'global_note' in stats:
			note = stats.get('global_note', None)
		if not note:
			try:
				note = eval(evaluation, {}, stats) # pylint: disable=eval-used
			except Exception as ex: # pylint: disable=broad-except
				note = 'NA'
		
		pnote = previous_stats.get('global_note', None)
		
		if not pnote:
			if previous_stats.get('statement', 0) == 0:
				pnote = 'NA'
			else:
				try:
					pnote = eval(evaluation, {}, previous_stats)
				except Exception as ex:
					pnote = 'NA'
		
		if isinstance(note, (int, float)) and isinstance(pnote, (int, float)):
			dnote = note - pnote
			
			dnote = '{:#.2f}'.format(dnote)
			note = '{:#.2f}'.format(note)
			pnote = '{:#.2f}'.format(pnote)
		else:
			dnote = 'NA'
			note = '{:#.2f}'.format(note)
		
		lines = ('stats', 'previous', 'difference') + (note, pnote, dnote)
		
		sect.append(Table(children=lines, cols=3, rheaders=1))
	
	def append_reports(self):
		self.reports.append(('RP6201', 'Evaluation', self.evaluation_callback))
	
	

#register_report,
@__all__.add
def options_by_file(file='options.yaml'):
	from startups import join
	import lintful
	stream = lintful.__loader__.get_data('options.yaml').decode()
	options = tuple(yaml.safe_load(stream))
	return options


@__all__.add
def find_lintfulrc():
	"""search the lintfulrc rc file and return its path if it find it, else None
	"""
	# is there a lintfulrc rc file in the current directory ?
	if os.path.exists('lintfulrc'):
		return os.path.abspath('lintfulrc')
	if os.path.exists('.lintfulrc'):
		return os.path.abspath('.lintfulrc')
	if os.path.isfile('__init__.py'):
		curdir = os.path.abspath(os.getcwd())
		while os.path.isfile(os.path.join(curdir, '__init__.py')):
			curdir = os.path.abspath(os.path.join(curdir, '..'))
			if os.path.isfile(os.path.join(curdir, 'lintfulrc')):
				return os.path.join(curdir, 'lintfulrc')
			if os.path.isfile(os.path.join(curdir, '.lintfulrc')):
				return os.path.join(curdir, '.lintfulrc')
	if 'LINTFULRC' in os.environ and os.path.exists(os.environ['LINTFULRC']):
		lintfulrc = os.environ['LINTFULRC']
	else:
		user_home = os.path.expanduser('~')
		if user_home == '~' or user_home == '/root':
			lintfulrc = '.lintfulrc'
		else:
			lintfulrc = os.path.join(user_home, '.lintfulrc')
			if not os.path.isfile(lintfulrc):
				lintfulrc = os.path.join(user_home, '.config', 'lintfulrc')
	if not os.path.isfile(lintfulrc):
		if os.path.isfile('/etc/lintfulrc'):
			lintfulrc = '/etc/lintfulrc'
		else:
			lintfulrc = None
	return lintfulrc








#add_option_group
#cb_set_provider_option
#add_optik_option
#cmdline_parser
#global_set_option
#load_command_line_configuration
#load_configuration
#load_configuration_from_config
#load_provider_defaults
#load_defaults
#option_groups
#optik_option
#options_by_section
#register_options_provider
#set_option

def check_file(option, opt, value):
	"""check a file value
	return the filepath
	"""
	from optparse import OptionValueError
	if os.path.exists(value):
		return value
	msg = "option %s: file %r does not exist"
	raise OptionValueError(msg % (opt, value))


def register(linter):
	"""required method to auto register this checker """
	linter.register_checker(Lint(linter))


if __name__ == '__main__': print(__file__)