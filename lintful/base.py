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

import pylint.lint
from pylint.utils import _splitstrip, _unquote, _MsgBase

TODO = ['PyLinter.set_current_module',
        'PyLinter.prepare_checkers',
        'open',
        'load_plugin_modules',
        'load_default_plugins',
        'get_ast',
        'generate_reports',
        'check_astroid_module',
        'self.reporter.on_set_current_module(modname, filepath)']

class ReporterMessageCOPY(_MsgBase):
	def __new__(cls, msg_id, symbol, location, msg, confidence, linter=None):
		linter = linter
		self = _MsgBase.__new__(
				cls, msg_id, symbol, msg, msg_id[0], MSG_TYPES[msg_id[0]],
				confidence, *location)
		if linter:
			if hasattr(linter, '_display'):
				self.linter = linter.linter
			else:
				self.linter = linter
		return self
	
	@classmethod
	def from_message(cls, message):
		msg_id = message.msg_id
		symbol = message.symbol
		location = (message.abspath, message.path, message.module, message.obj, message.line, message.column)
		msg = message.msg
		confidence = message.confidence
		return cls(msg_id, symbol, location, msg, confidence)
	
	@classmethod
	def from_kwargs(cls, kwargs):
		from startups.misc import itemgetter
		
		msg_id = kwargs.get('msg_id')
		symbol = kwargs.get('symbol')
		msg = kwargs.get('msg')
		confidence = kwargs.get('confidence')
		location = itemgetter('abspath', 'path', 'module', 'obj', 'line', 'column')(kwargs)
		return cls(msg_id, symbol, location, msg, confidence)
	
	def _asdict(self):
		from collections import OrderedDict
		
		d = OrderedDict(zip(self._fields, self))
		d['checker'] = self.checker
		d['fullname'] = self.fullname
		d['defn'] = self.defn
		return d
	
	def format(self, template):
		"""Format the message according to the given template.

		The template format is the one of the format method :
		cf. http://docs.python.org/2/library/string.html#formatstrings
		"""
		# For some reason, _asdict on derived namedtuples does not work with
		# Python 3.4. Needs some investigation.
		ndict = self._asdict()
		return template.format(**ndict)
	
	def set_linter(self, linter):
		if hasattr(linter, '_display'):
			self.linter = linter.linter
		else:
			self.linter = linter
	
	@property
	def confidence(self):
		return getattr(self[5], 'name', self[5])
	
	@property
	def checker(self):
		msg_id = self.msg_id or self.symbol
		if not hasattr(self, 'linter'):
			key = self.msg_id[1:3]
			return dict(CHECKER_IDS).get(key, '')
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).checker.name
			#self.__dict__['checker'] = name
			return name
	
	@property
	def defn(self):
		msg_id = self.msg_id or self.symbol
		if not hasattr(self, 'linter'):
			return ''
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).msg
			return name
	
	@property
	def fullname(self):
		return '.'.join([self.module, self.obj]).strip('.')
	
	@property
	def srcline(self):
		from linecache import getline
		
		sourceline = getline(self.abspath, self.line)[self.column:].rstrip()
		return sourceline
	
	def _re(self):
		string = self.defn
		msg = self.msg or ''
		
		escaped = regex.escape(string, special_only=True, literal_spaces=True)
		escaped = escaped.replace('%r', '\'(.*)\'')
		escaped = escaped.replace('%s', '(.*)')
		escaped = escaped.replace('%d', '(.*)')
		pattern = escaped or '(.+)'
		return regex.findall(pattern, msg)
	
	def __repr__(self):
		'Return a nicely formatted representation string'
		if self.fullname:
			template = '''(msg_id={msg_id!r}, symbol={symbol!r}, msg={msg!r}, fullname={fullname!r}, C={C!r}, confidence={confidence.name!r}, abspath={abspath!r}, line={line!r}, column={column!r}, checker={checker!r})'''
		else:
			template = '''(msg_id={msg_id!r}, symbol={symbol!r}, msg={msg!r}, C={C!r}, category={category!r}, confidence={confidence.name!r}, abspath={abspath!r}, path={path!r}, module={module!r}, obj={obj!r}, line={line!r}, column={column!r}, checker={checker!r}, fullname={fullname!r})'''
		
		return self.__class__.__name__ + template.format_map(self._asdict())


class Runner(object):
	def __init__(self, linter, args, reporter=None):
		self._rcfile = None
		self._plugins = []
		self._linter = linter
		try:
			pylint.lint.preprocess_options(args, {
				# option: (callback, takearg)
				'init-hook':        (pylint.lint.cb_init_hook, True),
				'rcfile':           (self.cb_set_rcfile, True),
				'load-plugins':     (self.cb_add_plugins, True),
			})
		except BaseException:
			pass
		self.options = (('rcfile',
		                 {'action': 'callback', 'callback': lambda *args: 1,
		                  'type': 'string', 'metavar': '<file>',
		                  'help': 'Specify a configuration file.'}),
		                ('init-hook',
		                 {'action': 'callback', 'callback': lambda *args: 1,
		                  'type': 'string', 'metavar': '<code>',
		                  'level': 1,
		                  'help': 'Python code to execute, usually for sys.path '
		                          'manipulation such as pygtk.require().'}),
		                )
		
		config_parser = linter.cfgfile_parser
		if config_parser.has_option('MASTER', 'init-hook'):
			cb_init_hook('init-hook', _unquote(config_parser.get('MASTER', 'init-hook')))
		if config_parser.has_option('MASTER', 'load-plugins'):
			plugins = _splitstrip(config_parser.get('MASTER', 'load-plugins'))
			linter.load_plugin_modules(plugins)
		linter.load_config_file()
		try:
			args = linter.load_command_line_configuration(args)
		except BaseException:
			pass
		
		
		self.args = args
	
	def cb_set_rcfile(self, name, value):
		"""callback for option preprocessing (i.e. before option parsing)"""
		self._rcfile = value
	
	def cb_add_plugins(self, name, value):
		"""callback for option preprocessing (i.e. before option parsing)"""
		from pylint.utils import _splitstrip
		self._plugins.extend(_splitstrip(value))
		
		
		
	def check(self):
		from pylint.lint import fix_import_path
		with fix_import_path(self.args):
			self.linter.check(self.args)
			self.linter.generate_reports()
	
del Runner



if __name__ == '__main__': print(__file__)