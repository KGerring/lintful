#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = base
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
import pylint.utils
import pylint.config
import pylint.lint

from pylint.reporters.text import colorize_ansi, ANSI_STYLES, ANSI_COLORS, ANSI_RESET
from pylint.interfaces import IReporter
from importpy.refactoring.pylint_checkers import ReporterMessage
from pylint.reporters.ureports.text_writer import TextWriter
from pylint.reporters import BaseReporter, CollectingReporter

from startups.helpers.decorators import ExportsList
from startups.misc import attrgetter
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


class Reporter(BaseReporter):
	"""
	A base-reporter to serve as a base-class for other reporters.
	It collects the raw-message, can print it to std.out, and
	works with the custom `ReporterMessage`, and a simple `display` feature.
	"""
	__implements__ = IReporter
	name = "custombase"
	
	def __init__(self, output=sys.stdout):
		"""Initializes with `messages`, and a holding container for
		options, and defaults.

		:param output: sys.stdout as default
		"""
		super(Reporter, self).__init__(output)
		#BaseReporter.__init__(self)
		self.messages = []
		self.options = dict()
		self.current_module = None
		self.current_file = None
		self.default_template = '{symbol}: {msg} ({fullname})|{abspath}:{line}:{column}'
		self._template = attrgetter('linter.config.msg_template')(self)
		if not self._template:
			self._template = self.default_template[:]
	
	#if FSTRINGS:
	#	self.fmt = f'{repr(symbol)}: {repr(msg)} ({fullname})|{abspath}:{line}:{column}'
	#else:
	#	self.fmt = self.default_template
	
	def get_manager(self, current_name):
		from astroid import MANAGER
		return MANAGER.astroid_cache.get(current_name)
	
	def clear(self):
		"""Clear the `messages` attribute of data"""
		self.messages.clear()
	
	def relative_path(path):
		comparepath = os.path.normcase(path)
		longest = ""
		for dir in sys.path:
			dir = os.path.normcase(dir)
			if comparepath.startswith(dir) and comparepath[len(dir)] == os.sep:
				if len(dir) > len(longest):
					longest = dir
		
		if longest:
			base = path[len(longest) + 1:]
		else:
			base = path
		
		drive, base = os.path.splitdrive(base)
		if os.altsep:
			base = base.replace(os.altsep, ".")
		return base
	
	def handle_message(self, msg):
		"""
		Correctly convert the msg based on how it is received, add it to `messages` and print to screen.
		:param msg:
		:return:
		"""
		from pylint import utils
		if isinstance(msg, (utils.Message, utils._MsgBase)):
			msg = ReporterMessage.from_message(msg)
		elif isinstance(msg, tuple):
			msg = ReporterMessage(*msg)
		
		elif isinstance(msg, dict):
			msg = ReporterMessage.from_kwargs(msg)
		
		elif isinstance(msg, ReporterMessage):
			msg.set_linter(self)
		
		else:
			msg = ReporterMessage.from_message(msg)
		
		msg.set_linter(self)
		self.messages.append(msg)
		self.write_message(msg)
	
	def write_message(self, msg, template=None):
		"""Convenience method to write a formated message with class default template"""
		if not template:
			template = self._template
		self.writeln(msg.format(template))
	
	def on_set_current_module(self, module, filepath):
		"""

		:param module:
		:param filepath:
		:return:
		"""
		self.current_module = module
		self.current_file = filepath
		self.current_ast = self.get_manager(module)
		
	
	def _display(self, layout):
		print(file=self.out)
		TextWriter().format(layout, self.out)
	
	def on_close(self, stats, previous_stats):
		"""Hook called when a module finished analyzing.
		
		previous_stats = config.load_results(self.file_state.base_name)
		self.reporter.on_close(self.stats, previous_stats)
		"""
		print('closed')


class ColorizedTemplate(object):
	"""A template class to get the ansi-codes to colorize messages to stdout"""
	blank_by_type = dict.fromkeys('CEFIRSW', (None, None))
	blank_by_attr = dict.fromkeys(pylint.utils.Message._fields, (None, None))
	colors = ANSI_COLORS
	styles = ANSI_STYLES
	
	def __init__(self, by_type=None, by_attr=None):
		#self.blank_by_type = dict.fromkeys('CEFIRW', (None, None))
		#self.blank_by_attr = dict.fromkeys(pylint.utils.Message._fields, (None, None))
		self.by_type = by_type or self.blank_by_type.copy()
		self.by_attr = by_attr or self.blank_by_attr.copy()
	
	def update_table(self, attr, color=None, style='', override = False):
		if color not in self.colors:
			color = None
		stylesplit = regex.split(',\s*', style)
		styleparts = [s for s in stylesplit if s in ANSI_STYLES]
		checkedstyle = ', '.join(styleparts)
		if checkedstyle is '':
			style = None
		
		if attr in self.by_type:
			self.by_type[attr] = (color, style)
		if attr in self.by_attr or override:
			self.by_attr[attr] = (color, style)
	
	def dump_table(self, filename):
		from startups.core import pickler
		
		table = dict(by_type=self.by_type, by_attr=self.by_attr)
		pickler(table, filename)
	
	def load_table(self, filename):
		from startups.core import unpickler
		
		try:
			table = unpickler(filename)
		except FileNotFoundError:
			table = dict()
		
		if 'by_type' in table:
			self.by_type = table.get('by_type', self.blank_by_type).copy()
		if 'by_attr' in table:
			self.by_attr = table.get('by_attr', self.blank_by_attr).copy()
	
	@classmethod
	def from_filename(cls, filename):
		self = cls()
		self.load_table(filename)
		return self


class ColorReporter(Reporter):
	name = "colored"
	by_type = False
	DEFAULT_COLOR_MAPPING = (('C', (None, 'bold')),
	                         ('E', ('red', 'bold')),
	                         ('F', ('red', 'bold, underline')),
	                         ('I', ('green', None)),
	                         ('R', ('magenta', 'bold, italic')),
	                         ('S', ('yellow', 'inverse')),
	                         ('W', ('blue', None)))
	
	def __init__(self, color_mapping = None, output = sys.stdout):
		Reporter.__init__(self)
		if not color_mapping:
			self.color_mapping = dict(self.DEFAULT_COLOR_MAPPING).copy()
		else:
			self.color_mapping = color_mapping
		if len(self.color_mapping) < 10:
			self.by_type = True
	
	def _get_decoration(self, attr):
		"""Returns the tuple color, style associated with msg_id as defined
		in self.color_mapping
		"""
		if self.by_type:
			key = attr[0]
		else:
			key = attr
		try:
			return self.color_mapping[key]
		except KeyError:
			return None, None
	
	def colorize_message(self, msg, *attrs):
		replacement_mapping = dict()
		if not attrs:
			attrs = ('msg', 'symbol', 'category', 'C')
			
		if self.by_type:
			color, style = self._get_decoration(msg.C)
			for attr in attrs:
				replacement_mapping[attr] = colorize_ansi(getattr(msg, attr), color, style)
			msg = msg._replace(**replacement_mapping)
			
		else:
			for attr in attrs:
				color, style = self._get_decoration(attr)
				replacement_mapping[attr] = colorize_ansi(getattr(msg, attr), color, style)
			msg = msg._replace(**replacement_mapping)
			
		return msg
	
	
	def write_message(self, msg, *attrs, template=None):
		"""Convenience method to write a formated message with class default template"""
		if not template:
			template = self._template
		if not attrs:
			colormsg = self.colorize_message(msg)
		else:
			colormsg = self.colorize_message(msg, *attrs)
		self.writeln(colormsg.format(template))
			
	@classmethod
	def from_template(cls, template, key = 'by_attr'):
		if isinstance(template, dict):
			if key in template:
				mapping = template.get(key)
			else:
				mapping = template
			
		elif isinstance(template, str) and os.path.exists(template):
			template = ColorizedTemplate.from_filename(template)
			mapping = getattr(template, key, None)
			
		else:
			mapping = None
			
		return cls(color_mapping = mapping)

a ='''
class PyLinterMixIn:
	manager = lambda x: MANAGER
	
	#args = collections.defaultdict(dict)
	
	
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
	
	def add_message(self, msg_descr, line=None, node=None, args=None, confidence=utils.UNDEFINED):
		"""Adds a message given by ID or name.

		If provided, the message string is expanded using args

		AST checkers should must the node argument (but may optionally
		provide line if the line number is different), raw and token checkers
		must provide the line argument.
		"""
		from pylint.exceptions import InvalidMessageError
		
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
			msg %= args
		# get module and object
		if node is None:
			module, obj = self.current_name, ''
			abspath = self.current_file
		else:
			module, obj = pylint.utils.get_module_and_frameid(node)
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
				pylint.utils.Message(msgid,
				              symbol,
				              (abspath, path, module, obj, line or 1, col_offset or 0), msg or '',
				              confidence)
		)
'''
		

def register(linter):
	"""Register the reporter classes with the linter."""
	linter.register_reporter(Reporter)
	linter.register_reporter(CollectingReporter)
	linter.register_reporter(ColorReporter)
	
	
	
	
	


if __name__ == '__main__': print(__file__)