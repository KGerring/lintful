#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = base
# author= KGerring
# date = 3/16/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = ['get_linter', '_do_load','LinterMixIn']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

import pylint.lint
from pylint.utils import _splitstrip, _unquote, _MsgBase, UNDEFINED
import pylint
from optparse import Values
TODO = ['PyLinter.set_current_module',
        'PyLinter.prepare_checkers',
        'open',
        'load_plugin_modules',
        'load_default_plugins',
        'get_ast',
        'generate_reports',
        'check_astroid_module',
        'self.reporter.on_set_current_module(modname, filepath)']

RCFILE = os.environ.get("PYLINTRC")

#from dictdiffer.utils import PathLimit




class LinterMixIn(object):
	""""""
	
	def _do_load(self):
		self.load_defaults()
		try:
			self.load_default_plugins()
		except Exception:
			pass
		config_file = getattr(self, 'config_file', config.PYLINTRC)
		self.read_config_file(config_file)
		
		if self.cfgfile_parser.has_option('MASTER', 'load-plugins'):
			plugins = utils._splitstrip(self.cfgfile_parser.get('MASTER', 'load-plugins'))
			self.load_plugin_modules(plugins)
		
		self.load_config_file()
		print('SETUP!')
		
	@property
	def config_parser(self):
		if hasattr(self, 'cfgfile_parser'):
			return getattr(self, 'cfgfile_parser')
		return None
	
	def add_message(self, msg_descr, line=None, node=None, args=None, confidence=pylint.utils.UNDEFINED):
		"""Adds a message given by ID or name.

		If provided, the message string is expanded using args

		AST checkers should must the node argument (but may optionally
		provide line if the line number is different), raw and token checkers
		must provide the line argument.
		"""
		from pylint.exceptions import InvalidMessageError
		from pylint import utils
		
		msg_info = self.msgs_store.check_message_id(msg_descr)
		msgid = msg_info.msgid
		# backward compatibility, message may not have a symbol
		symbol = msg_info.symbol or msgid
		# Fatal messages and reports are special, the node/scope distinction
		# does not apply to them.
		if msgid[0] not in utils._SCOPE_EXEMPT:
			if msg_info.scope == utils.WarningScope.LINE:
				if line is None:
					print(InvalidMessageError(
							'Message %s must provide line, got None' % msgid))
					pass
				if node is not None:
					print(InvalidMessageError(
							'Message %s must only provide line, '
							'got line=%s, node=%s' % (msgid, line, node)))
					pass
			elif msg_info.scope == utils.WarningScope.NODE:
				# Node-based warnings may provide an override line.
				if node is None:
					print(InvalidMessageError(
							'Message %s must provide Node, got None' % msgid))
					pass
		
		if line is None and node is not None:
			line = node.fromlineno
		if hasattr(node, 'col_offset'):
			col_offset = node.col_offset # XXX measured in bytes for utf-8, divide by two for chars?
		else:
			col_offset = None
		# should this message be displayed
		if not self.is_message_enabled(msgid, line, confidence):
			self.file_state.handle_ignored_message(
					self.get_message_state_scope(msgid, line, confidence),
					msgid, line, node, args, confidence)
			return
		# update stats
		msg_cat = utils.MSG_TYPES[msgid[0]]
		self.msg_status |= utils.MSG_TYPES_STATUS[msgid[0]]
		self.stats[msg_cat] += 1
		self.stats['by_module'][self.current_name][msg_cat] += 1
		try:
			self.stats['by_msg'][symbol] += 1
		except KeyError:
			self.stats['by_msg'][symbol] = 1
		# expand message ?
		msg = msg_info.msg
		if args:
			try:
				msg %= args
			except TypeError:
				if msgid == 'W0614':
					msg = args[:]
				else:
					msg = msg + ', '.join([repr(arg) for arg in args])
		
		# get module and object
		if node is None:
			module, obj = self.current_name, ''
			abspath = self.current_file
		else:
			module, obj = utils.get_module_and_frameid(node)
			abspath = node.root().file
		
		if not hasattr(self.reporter, 'path_strip_prefix'):
			path = abspath
		else:
			path = abspath.replace(self.reporter.path_strip_prefix, '')
		
		if args:
			path = args
		
		#if symbol not in self.args[self.current_name]:
		#    self.args[self.current_name][symbol] = list()
		#
		#self.args[self.current_name][symbol].append(dict(line=line, node=node, args=args))
		
		# add the message
		self.reporter.handle_message(
				utils.Message(msgid,
				              symbol,
				              (abspath, path, module, obj, line or 1, col_offset or 0), msg or '',
				              confidence)
		)
	
def _do_load(linter):
	"""
	Workaround if the patched pylint.lint doesn't exist (i.e No PyLinterMixIn class).
	:param linter:
	:return:
	"""
	from pylint import config
	from pylint.utils import _splitstrip
	linter.load_defaults()
	try:
		linter.load_default_plugins()
	except Exception:
		pass
	config_file = getattr(linter, 'config_file', config.PYLINTRC)
	linter.read_config_file(config_file)
	
	if linter.cfgfile_parser.has_option('MASTER', 'load-plugins'):
		plugins = _splitstrip(linter.cfgfile_parser.get('MASTER', 'load-plugins'))
		linter.load_plugin_modules(plugins)
	
	linter.load_config_file()
	print('External "_do_load" complete!', file = sys.stderr)


def get_linter(rcfile = RCFILE):
	from pylint.lint import PyLinter
	linter = PyLinter(pylintrc= rcfile)
	if hasattr(linter, '_do_load'):
		linter._do_load()
	else:
		_do_load(linter)
		
	return linter
	






if __name__ == '__main__': print(__file__)