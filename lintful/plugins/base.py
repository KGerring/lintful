#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = base
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['ReporterMessage', 'Reporter', 'ColorizedTemplate', 'ColorReporter']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import pylint.utils
import pylint.config
import pylint.lint
import collections
from pylint.reporters.text import colorize_ansi, ANSI_STYLES, ANSI_COLORS, ANSI_RESET
from pylint.interfaces import IReporter
from pylint.reporters.ureports.text_writer import TextWriter
from pylint.reporters import BaseReporter, CollectingReporter

from startups.helpers.decorators import ExportsList
from startups.misc import attrgetter
from startups.core import OrderedSet
from pylint.utils import _MsgBase, MSG_TYPES, Message, UNDEFINED

__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


class cached_property(object):
	def __init__(self, func):
		self.func = func
	
	#for attr in ('__name__', '__module__', '__doc__'):
	#    setattr(self, attr, getattr(func, attr, None))
	
	def __get__(self, obj, cls=None):
		if obj is None:
			return self
		value = self.func(obj)
		object.__setattr__(obj, self.func.__name__, value)
		#obj.__dict__[self.func.__name__] = value = self.func(obj)
		return value

CHECKER_IDS = (('00', 'master'),
               ('01', 'basic'),
               ('02', 'refactoring'),
               ('03', 'format'),
               ('04', 'spelling'),
               ('05', 'miscellaneous'),
               ('06', 'variables'),
               ('07', 'exceptions'),
               ('08', 'similarities'),
               ('09', 'design'),
               ('10', 'newstyle'),
               ('11', 'iterable_check'),
               ('12', 'logging'),
               ('13', 'string'),
               ('14', 'string_constant'),
               ('15', 'stdlib'),
               ('16', 'python3'),
               ('17', 'refactoring'),
               ('18', 'len'),
               ('90', 'parameter_documentation'),
               
               )
CHECKER_ID_EXCEPTIONS = (
	('docstyle', ('C0199', 'C0198', 'bad-docstring-quotes', 'docstring-first-line-empty'), '01'),
	('mccabe'  ,('R1260', 'too-complex'), '12'),

                          )
CODE_ATTRIBUTES = ('co_argcount',
                   'co_kwonlyargcount',
                   'co_nlocals',
                   'co_stacksize',
                   'co_flags',
                   'co_code',
                   'co_consts',
                   'co_names',
                   'co_varnames',
                   'co_filename',
                   'co_name',
                   'co_firstlineno',
                   'co_lnotab',
                   'co_freevars',
                   'co_cellvars')

class CodeTuple(collections.namedtuple('code', CODE_ATTRIBUTES)):
	"""
	Represent a `code` object as a namedtuple.
	"""
	
	def __new__(cls, co_argcount=0, co_kwonlyargcount=0, co_nlocals=0,
	            co_stacksize=0, co_flags=0, co_code=b'',
	            co_consts=(), co_names=(),
	            co_varnames=(), co_filename='', co_name='',
	            co_firstlineno=0, co_lnotab=b'',
	            co_freevars=(), co_cellvars=()):
		"""Create new instance of CodeTuple() with default values"""
		from builtins import property as _property, tuple as _tuple
		
		return _tuple.__new__(cls, (
			co_argcount, co_kwonlyargcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames,
			co_filename, co_name, co_firstlineno, co_lnotab, co_freevars, co_cellvars))


MESSAGE_ATTRIBUTES = ('msg_id',
 'symbol',
 'msg',
 'C',
 'category',
 'confidence',
 'abspath',
 'path',
 'module',
 'obj',
 'line',
 'column',
 'checker',
 'fullname',
 'defn')










import dataclasses
field = dataclasses.field

#dataclasses.make_dataclass('Message', MESSAGE_ATTRIBUTES, order=True, hash = True)

FIELD = dataclasses.field(default = '', init = True, repr = True, hash = True, compare = True, metadata = {})
FIELD.type = str

NONE_FIELD = dataclasses.field(default=None, hash=True, metadata={})
NONE_FIELD.type = str


from pylint.interfaces import CONFIDENCE_LEVELS, Confidence


@dataclasses.dataclass
class MessageData:
	
	msg_id: str     = field(default ='E0001',       hash=True, metadata = {})
	symbol: str     = field(default ='syntax-error',hash=True, metadata = {})
	msg: str        = field(default ='%s',          hash=True, metadata = {})
	C: str          = field(default ='E',           hash=True, metadata = {})
	category: str   = field(default ='error',       hash=True, metadata = {"MSG_TYPES": MSG_TYPES})
	confidence: tuple = field(default =('UNDEFINED',),     hash=True,)# metadata = dict(CONFIDENCE_LEVELS =CONFIDENCE_LEVELS))
	abspath: str    = field(default = '',           hash=True, metadata = {})
	path: str       = field(default='',             hash=True, metadata = {})
	module: str     = field(default='',             hash=True, metadata = {})
	obj: str        = field(default='',             hash=True, metadata = {})
	line: int       = field(default = 1,            hash=True, metadata = {})
	column:int      = field(default = 0,            hash=True, metadata = {})
	#checker: str    = field(default = None, init = False, hash=True, metadata = dict(CHECKER_IDS=CHECKER_IDS))
	#fullname: str   = field(default = None, init = False,hash=True, metadata = None)
	#defn: str       = field(default = None, init=False,hash=True, metadata = {})
	
	
	def set_linter(self, linter):
		if hasattr(linter, '_display'):
			setattr(self, 'linter', linter.linter)
		else:
			setattr(self, "linter",linter)
	
	#@property
	#def _fields(self):
	#	return tuple(self.__dataclass_fields__)
	#
	#def _asdict(self):
	#	from collections import OrderedDict
	#	d = OrderedDict(zip(self._fields, self))
	#
	@cached_property
	def fullname(self):
		name = '.'.join([self.module, self.obj]).strip('.')
		self.__dataclass_fields__['fullname'] = FIELD
		self.__dataclass_fields__['fullname'].name = 'fullname'
		return name
	
	@cached_property
	def checker(self):
		self.__dataclass_fields__['checker'] = FIELD
		self.__dataclass_fields__['checker'].name = "checker"
		
		msg_id = self.msg_id or self.symbol
		if not hasattr(self, 'linter'):
			key = self.msg_id[1:3]
			return dict(CHECKER_IDS).get(key, '')
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).checker.name
			#self.__dict__['checker'] = name
			return name
	
	
	@cached_property
	def defn(self):
		self.__dataclass_fields__['defn'] = FIELD
		self.__dataclass_fields__['defn'].name = 'defn'
		msg_id = self.msg_id or self.symbol
		if not hasattr(self, 'linter'):
			return '%s'
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).msg
			return name


class ReportMessage(MessageData):
	pass


class _ReporterMessage(collections.namedtuple('message', MESSAGE_ATTRIBUTES)):
	
	def __new__(cls, msg_id='E0001', symbol='syntax-error', msg='%s', C='E', category='error',
	            confidence='UNDEFINED', abspath='', path='', module='', obj='', line=1,
	            column=0, checker='master', fullname='', defn='%s'):
		from builtins import tuple as _tuple
		
		return _tuple.__new__(cls, (
		msg_id, symbol, msg, C, category, confidence, abspath, path,
		module, obj, line, column, checker, fullname, defn))
		
		
	
class ReporterMessage(pylint.utils._MsgBase):
	
	#def __new__(cls, msg_id ='E0001', symbol = '', location =('','','','',1,0), msg='', confidence='', linter=None):
	
	def __new__(cls, *args, **kwargs):
		if len(args) == 5:
			msg_id, symbol, location, msg, confidence = args
			self = _MsgBase.__new__(
					cls, msg_id, symbol, msg, msg_id[0], MSG_TYPES[msg_id[0]],
					confidence, *location)
			
		#elif len(args) == 12:
		else:
			self = _MsgBase.__new__(cls, *args)
			
		if kwargs:
			self.__dict__.update(kwargs)
		
		return self
			
	
	def _new_(cls, msg_id, symbol, location, msg, confidence, **kwargs):
		
		linter = kwargs.pop('linter', None)
		self = _MsgBase.__new__(
				cls, msg_id, symbol, msg, msg_id[0], MSG_TYPES[msg_id[0]],
				confidence, *location)
		self.set_linter(linter)
		#if linter:
		#	if hasattr(linter, '_display'):
		#		self.linter = linter.linter
		#	else:
		#		self.linter = linter
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
	def from_tuple(cls, tuple_):
		return _MsgBase.__new__(cls, *tuple_)
		
	@classmethod
	def from_kwargs(cls, kwargs):
		from startups.misc import itemgetter
		
		linter = kwargs.pop('linter', None)
		msg_id = kwargs.get('msg_id')
		symbol = kwargs.get('symbol')
		msg = kwargs.get('msg')
		confidence = kwargs.get('confidence')
		location = itemgetter('abspath', 'path', 'module', 'obj', 'line', 'column')(kwargs)
		return cls(msg_id, symbol, location, msg, confidence, linter = linter)
	
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
	
	def set_linter(self, linter = None):
		if linter:
			if hasattr(linter, '_display'):
				setattr(self, "linter", linter.linter)
			else:
				setattr(self, "linter", linter)
		else:
			setattr(self, "linter", None)
			
	
	@cached_property
	def _confidence(self):
		return getattr(self[5], 'name', self[5])
	
	@cached_property
	def checker(self):
		msg_id = self.msg_id or self.symbol
		if not getattr(self, 'linter', None):
			key = self.msg_id[1:3]
			return dict(CHECKER_IDS).get(key, '')
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).checker.name
			#self.__dict__['checker'] = name
			return name
		
	@cached_property
	def defn(self):
		msg_id = self.msg_id or self.symbol
		if not getattr(self, 'linter', None):
			return '%s'
		else:
			name = self.linter.msgs_store.check_message_id(msg_id).msg
			return name
		
	@cached_property
	def fullname(self):
		return '.'.join([self.module, self.obj]).strip('.')
		
	@cached_property
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
		
		ddict = self._asdict()
		_confidence = ddict.get('confidence','UNDEFINED')
		if hasattr(_confidence, 'name'):
			ddict['confidence'] = getattr(_confidence, 'name', 'UNDEFINED')
		
		if self.fullname:
			template = '''(msg_id={msg_id!r}, symbol={symbol!r}, msg={msg!r}, fullname={fullname!r}, C={C!r}, confidence={confidence!r}, abspath={abspath!r}, line={line!r}, column={column!r}, checker={checker!r})'''
		else:
			
			template = '''(msg_id={msg_id!r}, symbol={symbol!r}, msg={msg!r}, C={C!r}, category={category!r}, confidence={confidence!r}, abspath={abspath!r}, path={path!r}, module={module!r}, obj={obj!r}, line={line!r}, column={column!r}, checker={checker!r}, fullname={fullname!r})'''
		
		return self.__class__.__name__ + template.format_map(self._asdict())
	
	def __getstate__(self):
		return self._asdict()
	
	def __setstate__(self, state):
		return self.from_kwargs(state)
		
	def __getnewargs_ex__(self):
		asdict = self._asdict()
		checker = asdict.pop('checker',None)
		fullname = asdict.pop('fullname', None)
		defn = asdict.pop('defn', None)
		
		keywords = dict(checker =checker, fullname =fullname, defn =defn)
		positional = tuple(self)
		
		return (positional, keywords)
		


class Reporter(BaseReporter):
	"""
	A base-reporter to serve as a base-class for other reporters.
	It collects the raw-message, can print it to std.out, and
	works with the custom `ReporterMessage`, and a simple `display` feature.
	"""
	__implements__ = IReporter
	name = "custombase"
	options = dict(module=set([]))
	line_format = '{symbol}: {msg} ({fullname})|{abspath}:{line}:{column}'
	
	def __init__(self, output=sys.stdout):
		"""Initializes with `messages`, and a holding container for
		options, and defaults.

		:param output: sys.stdout as default
		"""
		super(Reporter, self).__init__(output)
		#BaseReporter.__init__(self)
		self.messages = OrderedSet([])
		self.msgs = self.messages.items
		self.options = dict(module = set([]))
		self.current_module = None
		self.current_file = None
		self.default_template = '{symbol}: {msg} ({fullname})|{abspath}:{line}:{column}'
		self._template = attrgetter('linter.config.msg_template')(self)
		if not self._template:
			self._template = self.line_format[:]
		
		self.nodes = collections.defaultdict(set)
	#if FSTRINGS:
	#	self.fmt = f'{repr(symbol)}: {repr(msg)} ({fullname})|{abspath}:{line}:{column}'
	#else:
	#	self.fmt = self.default_template
	
	@property
	def current_name(self):
		if not self.current_module:
			return self.linter.current_name
		else:
			return self.current_module
	
	def get_manager(self, current_name = None):
		from astroid import MANAGER
		if not current_name:
			return MANAGER.astroid_cache
		#return MANAGER.ast_from_module_name(current_name)
		ast =  MANAGER.astroid_cache.get(current_name, None)
		if not ast:
			ast =  MANAGER.ast_from_module_name(current_name)
		return ast
		
		
	
	def clear(self):
		"""Clear the `messages` attribute of data"""
		self.messages.clear()
	
	@staticmethod
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
	
	def handle_node(self, msg_info, node):
		""""""
		mid = msg_info.symbol or msg_info.msgid
		scope = getattr(msg_info, 'scope', 'line-based-msg')
		if scope == 'node-based-msg':
			self.nodes[mid].add(node)
	
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
			if len(msg) == 12:
				msg = ReporterMessage.from_tuple(msg)
			else:
				msg = ReporterMessage(*msg)
		
		elif isinstance(msg, dict):
			msg = ReporterMessage.from_kwargs(msg)
		
		elif isinstance(msg, ReporterMessage):
			msg.set_linter(self)
		
		else:
			msg = ReporterMessage.from_message(msg)
		
		msg.set_linter(self)
		
		if msg.module not in self.options['module']:
			self.options['module'].add(msg.module)
			
		self.messages.append(msg)
		self.write_message(msg)
	
	def write_message(self, msg, template=None):
		"""Convenience method to write a formated message with class default template"""
		if not template:
			template = self._template
		self.writeln(msg.format(template))
			
	
	def on_set_current_module(self, module, filepath = None):
		"""

		:param module:
		:param filepath:
		:return:
		"""
		self.current_module = module
		self.current_file = filepath
		self.current_ast = self.get_manager(module)
		self._template = self.linter.config.msg_template or self.line_format
		
	def _display(self, layout):
		print(file=self.out)
		TextWriter().format(layout, self.out)
	
	def on_close(self, stats, previous_stats):
		"""Hook called when a module finished analyzing.
		if self.file_state.base_name is not None:
			previous_stats = config.load_results(self.file_state.base_name)
			self.reporter.on_close(self.stats, previous_stats)
			if self.config.reports:
				sect = self.make_reports(self.stats, previous_stats)
			if self.config.persistent:
				config.save_results(self.stats, self.file_state.base_name)
		else:
			self.reporter.on_close(self.stats, {})
			
			
		data_file = _get_pdata_path(base, 1)
			
		"""
		#persistent-amount
		linter = self.linter
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
		stylesplit = regex.split(r',\s*', style)
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
	DEFAULT_COLOR_MAPPING = (('C', ('cyan', None)),
	                         ('E', ('red', None)),
	                         ('F', ('red', 'italic, underline')),
	                         ('I', ('green', None)),
	                         ('R', ('magenta', 'italic')),
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
	
	
	def write_message(self, msg, *attrs, template=None):    # pylint: disable=W0221
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

	


#class Serializer(object):
#	@dispatch_on('obj')
#	def dump(self, obj):
#		return obj


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
del a


def register(linter):
	"""Register the reporter classes with the linter."""
	linter.register_reporter(Reporter)
	linter.register_reporter(CollectingReporter)
	linter.register_reporter(ColorReporter)
	
	
	


if __name__ == '__main__': print(__file__)