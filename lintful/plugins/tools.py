#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = ['MessageComp', 'MESSAGE_FIELDS', 'Container',
           'Fielder', 'MessagesSorter', 'lookup', 'make_flat_key', 'iclassmethod', 'MessageList', '_groupby',
           'grouped']

__all__.sort()

import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
#from pylint.interfaces import implements as pylint_implements, IReporter

from addict import Dict
from collections import (
    _Link, _proxy, ChainMap, defaultdict, deque, MutableMapping,
    MutableSequence, MutableSet, OrderedDict,)
import collections
import dictdiffer
#import dictdiffer.conflict
#import dictdiffer.merge
#import dictdiffer.resolve
#import dictdiffer.unify
import dictdiffer.utils  # create_dotted_node
from functools import cmp_to_key, total_ordering
import itertools
from itertools import chain
from lintful.plugins.base import ReporterMessage
from pstats import TupleComp
from sphinx.ext.inheritance_diagram import import_classes
from startups.helpers.decorators import return_as
from startups.misc import attrgetter
from toolz import groupby  # , getter
import dpath
from types import DynamicClassAttribute

#import six

#from zope.interfaces import Interface

#__all__ = ExportsList(initlist=_all_[:], __file__=__file__)   # all-decorator: _all_

PathLimit = dictdiffer.utils.PathLimit



P = PathLimit([('symbol', 'column')])

BASE_MESSAGE_FIELDS = [(0, 'msg_id'),
                       (1, 'symbol'),
                       (2, 'msg'),
                       (3, 'C'),
                       (4, 'category'),
                       (5, 'confidence'),
                       (6, 'abspath'),
                       (7, 'path'),
                       (8, 'module'),
                       (9, 'obj'),
                       (10, 'line'),
                       (11, 'column'),]

MESSAGE_FIELDS = BASE_MESSAGE_FIELDS+ [(12, 'checker'),(13, 'fullname')]



#recurred = diff(first[key], second[key], node=node + [key],
#                ignore=ignore, path_limit=path_limit, expand=expand, tolerance=tolerance)

#t.dictdiffer.dot_lookup(d, ['symbol', 'reimported', '2'], False)
#t.dictdiffer.dot_lookup(d, 'symbol.reimported.2')
#t.dictdiffer.dot_lookup(d, 'symbol.reimported.2', True)
#sorted(t.dictdiffer.dot_lookup(d, 'symbol.reimported', False))
#t.dictdiffer.dot_lookup(m, '2', False)



class Fielder(object):
	_field_names = ReporterMessage._fields
	#__slots__ = ['__dict__', '__weakref__', 'field', 'field_list', 'field_order']
	
	def __init__(self, **kwargs):
		self.field = kwargs.get('field', None)
		self.field_list = kwargs.get('fields_list', dict())
		
		if not bool(self.field_list):
			self.field_list = kwargs.get('field_list', dict())
			
		self.field_order = kwargs.get('field_order', list(self.field_list))
		self._field_names = ReporterMessage._fields

		self._kwargs = kwargs.copy()
		
		#for slot in self.__slots__[2:]:
		#	self.__dict__[slot] = getattr(self, slot, None)
		
		
	@property
	def fields_list(self):
		return getattr(self, 'field_list', {})
	
	
	
		#if isinstance(args[0], dict):
		#	self.field_list.update(args[0])
		#
		#
		#elif isinstance(args[0], (list, tuple)):
		#	self.field_order = args[0]
		#	self.field = self.field_order[-1]
		#
		#elif isinstance(args[0], str):
		#	self.field = args[0]
		#	self.field_list = [self.field]

class FieldError(Exception):
	"""base exception class for all astroid related exceptions

	AstroidError and its subclasses are structured, intended to hold
	objects representing state when the exception is thrown.  Field
	values are passed to the constructor as keyword-only arguments.
	Each subclass has its own set of standard fields, but use your
	best judgment to decide whether a specific exception instance
	needs more or fewer fields for debugging.  Field values may be
	used to lazily generate the error message: self.message.format()
	will be called with the field names and values supplied as keyword
	arguments.
	"""
	
	def __init__(self, message='field {field!r} not found', **kws):
		super(FieldError, self).__init__(message)
		self.message = message
		for key, value in kws.items():
			setattr(self, key, value)
	
	def __str__(self):
		return self.message.format(**vars(self))


class Container(list):
	"""

	"""
	_field_names = ReporterMessage._fields
	
	def __init__(self, *args, **kwargs):
		"""

		:param args:
		:param kwargs: `field`,`fields_list`, `field_dict`, `field_order`,`__parent`, `__key`
		"""
		self.field = kwargs.pop('field', None)
		self.fields_list = kwargs.pop('fields_list', [])
		
		self.field_dict = kwargs.pop('field_dict', dict())
		if self.field:
			self.field_dict.setdefault(self.field, {})
		
		self.field_order = kwargs.pop('field_order', [])
		if self.field:
			self.field_order.append(self.field)
		
		#self.root = _Link()
		#self.root.key = self.field
		object.__setattr__(self, '__parent', kwargs.pop('__parent', None))
		object.__setattr__(self, '__key', kwargs.pop('__key', None))
		
		for arg in args:
			if not arg:
				continue
			elif isinstance(arg, dict):
				for key, val in arg.items():
					self[key] = self._hook(val)
			
			elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
				self[arg[0]] = self._hook(arg[1])
			
			elif isinstance(arg, list):
				super().__init__(arg)
			else:
				for key, val in iter(arg):
					self[key] = self._hook(val)
		
		for key, val in kwargs.items():
			setattr(self, key, val)
		
		self.__hardroot = _Link()
		self.__root = root = _proxy(self.__hardroot)
		root.prev = root.next = root
		self.__map = vars(self)
	
	#L.index(value, [start, [stop]])
	
	
	@classmethod
	def _hook(cls, item):
		if isinstance(item, dict):
			return cls(item)
		#elif isinstance(item, (list, tuple)):
		#	return type(item)(cls._hook(elem) for elem in item)
		return item
	
	def get(self, name):
		if name not in self:
			return Container(__parent=self, __key=name)
		return super(Container, self).__getitem__(name)
	
	#setdefault(name, []).append(stmt)
	
	def __setitem__(self, name, value):
		#cc.__parent.__getitem__('W0612')
		
		super(Container, self).__setitem__(name, value)
		try:
			p = object.__getattribute__(self, '__parent')
			key = object.__getattribute__(self, '__key')
		except AttributeError:
			p = None
			key = None
		if p is not None:
			p[key] = self
			object.__delattr__(self, '__parent')
			object.__delattr__(self, '__key')
	
	def _get_field_names(self):
		"""
		return `self._field_names`
		:return:


		"""
		return self._field_names
	
	def validate_field(self, name):
		if name in self._field_names:
			return True
		raise FieldError(field=name)
	
	def __getitem__(self, key):
		if isinstance(key, tuple) and len(key) == 2:
			results = self.__class__()
			attr, val = key
			for item in self:
				if getattr(item, attr) == val:
					results.append(item)
			return self.__class__(results, field=attr, __parent=self, __key=val)
		
		elif isinstance(key, str):
			self.validate_field(key)
			results = _groupby(key, self)
			
			return self.__class__(self, field=key, __parent=results)
		
		
		elif isinstance(key, int):
			return list.__getitem__(self, key)
		
		elif key not in self:
			return Container(__parent=self, __key=key)
		else:
			return list.__getitem__(self, key)
	
	def __getslice__(self, i, j):
		return self[i][j]
	
	def __set_item__(self, key, value):
		super(Container, self).__setitem__(key, value)


class MessageContainer(MutableSequence):
	"""
	A container for ReporterMessages
	"""
	
	def __init__(self, *data, field=None, **kwargs):
		self.field = field
		if isinstance(self.field, (list, tuple)):
			self.field = list(self.field)
		
		#self.field_order = kwargs.pop('field_order', [])
		#self.field = kwargs.pop('field', None)
		object.__setattr__(self, '__parent', kwargs.pop('__parent', None))
		object.__setattr__(self, '__key', kwargs.pop('__key', None))
		
		self.__hardroot = _Link()
		self.__root = root = _proxy(self.__hardroot)
		root.prev = root.next = root
		self.__map = vars(self)
		
		self._field_names = ReporterMessage._fields
		self.mapping = dict()
		self.items = []
		
		for key, val in kwargs.items():
			self.mapping[key] = val
			setattr(self, key, val)
		root.key = self.field
		
		self.fields_list = kwargs.pop('fields_list', dict())
		
		if self.field and not bool(self.fields_list):
			self.fields_list.setdefault(self.field, {})
		
		self.field_order = kwargs.pop('field_order', [])
		if self.field:
			self.field_order.append(self.field)
		
		if isinstance(data, MessageContainer):
			self.items += data.items
		elif isinstance(data, list):
			self.items += data
			
		else:
			self.items = list(data)
			if len(self.items) == 1 and isinstance(self.items[0], dict):
				self.items = self.items[0]
		
			
		
		
		#for arg in args:
		#	if not arg:
		#		continue
		#	if isinstance(arg, MessageContainer):
		#		self.items += arg.items
		#
		#	elif isinstance(arg, list):
		#		self.items += arg
		
		#for key, val in kwargs.items():
		#	self.mapping[key] = val
		#	setattr(self, key, val)
		#self[key] = self._hook(val)
		#super(MessageContainer, self).__init__(*args, **kwargs)
	
	@classmethod
	def _hook(cls, item):
		if isinstance(item, dict):
			return cls(item)
		elif isinstance(item, (list, tuple)):
			return type(item)(cls._hook(elem) for elem in item)
		return item
	
	def __setitem__(self, key, value):
		return list.__setitem__(self.items, key, value)
	
	def __getitem__(self, key):
		if isinstance(key, tuple) and len(key) == 2:
			return None
		
		elif isinstance(key, int):
			return list.__getitem__(self.items, key)
		else:
			return list.__getitem__(self.items, key)
	
	def __delitem__(self, key):
		return list.__delitem__(self.items, key)
	
	def __len__(self):
		return len(self.items)
	
	def insert(self, index, object):
		return list.insert(self.items, index, object)


class _Cont(MutableMapping, MutableSequence):
	def __init__(self, *args, **kwargs):
		self.items = args[0]
		self.mapping = kwargs.copy()
		object.__setattr__(self, '__parent', kwargs.pop('__parent', None))
		object.__setattr__(self, '__key', kwargs.pop('__key', None))
		
		for arg in args:
			if not arg:
				continue
			elif isinstance(arg, dict):
				for key, val in arg.items():
					self[key] = self._hook(val)
			
			elif isinstance(arg, tuple) and (not isinstance(arg[0], tuple)):
				self[arg[0]] = self._hook(arg[1])
			else:
				for key, val in iter(arg):
					self[key] = self._hook(val)
	
	@classmethod
	def _hook(cls, item):
		if isinstance(item, dict):
			return cls(item)
		elif isinstance(item, (ReporterMessage, Container)):
			return item
		elif isinstance(item, (list, tuple)):
			return type(item)(cls._hook(elem) for elem in item)
		return item
	
	def __setitem__(self, key, value):
		return list.__setitem__(self.items, key, value)
	
	def __getitem__(self, key):
		return list.__getitem__(self.items, key)
	
	def __len__(self):
		return len(self.items)
	
	def insert(self, index, object):
		return list.insert(self.items, index, object)
	
	def __delitem__(self, key):
		return list.__delitem__(self.items, key)


class iclassmethod(object):
	'''Descriptor for method which should be available as class method if called
	on the class or instance method if called on an instance.
	'''
	
	def __init__(self, func):
		self.func = func
	
	def __get__(self, instance, objtype):
		import types
		
		if instance is None:
			return types.MethodType(self.func, objtype)
		return types.MethodType(self.func, instance)
	
	def __set__(self, instance, value):
		raise AttributeError("can't set attribute")


def make_flat_key(node, delimiter=':'):
	"""

	:param list node: A list of keys
	:param str delimiter: A delimiter to join the keys
	:return: A flattened key

	>>> make_flat_key(['unused-import', 'plugins.utils', "2"])
	'unused-import:plugins.utils:2'
	>>> make_flat_key(['unused-import', 'plugins.utils', 2])
	['unused-import', 'plugins.utils', 2]
	>>> make_flat_key(['unused-import', 'utils'], delimiter='/')
	'unused-import/utils'
	"""
	if all(map(lambda x: isinstance(x, str), node)):
		return delimiter.join(node)
	else:
		return list(node)


def lookup(source, lookup='', parent=False, delimiter=':'):
	"""

	:param dict source: The dictionary to lookup on
	:param lookup: A list of keys or a delimited joined key
	:param bool parent: If to return the parent dictionary of the result
	:param str delimiter: The delimiter the lookup is joined with
	:return: A lookup to the source

	>>> dic = {'a': {'b': 'hello'}}
	>>> lookup(dic, 'a:b', parent = True)
	{'b': 'hello'}
	>>> lookup(dic, 'a:b', parent = False)
	'hello'
	>>> lookup(dic, [])
	{'a': {'b': 'hello'}}
	>>> lookup(dic, 'a/b', parent=True, delimiter='/')
	{'b': 'hello'}
	"""
	if lookup is None or lookup == '' or lookup == []:
		return source
	value = source
	if isinstance(lookup, str):
		keys = lookup.split(delimiter)
	
	elif isinstance(lookup, (list, tuple)):
		keys = list(lookup)
	
	if parent:
		keys = keys[:-1]
	
	for key in keys:
		if isinstance(value, list):
			key = int(key)
		value = value[key]
	return value


class MessageList(MutableSequence, MutableMapping):
	_delimiter = ':'
	_field_names = ReporterMessage._fields
	

	
	def __init__(self, *args, **kwargs):
		self.data = []
		
		self._fielder = kwargs.pop('fielder', Fielder(**kwargs))

		self.field = kwargs.pop('field', None)
		self.fields_list = kwargs.pop('fields_list', {})
		self.field_order = kwargs.pop('field_order', [])
		
		self.mapping = kwargs.copy()
		#self.__dict__ = kwargs.copy()
		
		self._keys = set([])
		
		for arg in args:
			if not arg:
				continue
			
			elif isinstance(arg, dict):
				for key, val in arg.items():
					self[key] = self._hook(val)
					self._keys.add(key)
			
			elif isinstance(arg, list):
				self.data += arg
			
			elif isinstance(arg, ReporterMessage):
				self.data.append(arg)
		
		for key, val in kwargs.items():
			setattr(self, key, val)
		
		for slot in self.__slots__[1:]:
			self.__dict__[slot] = getattr(self, slot, None)
	
	@classmethod
	def _hook(cls, item):
		if isinstance(item, dict):
			return cls(item)
		elif isinstance(item, (ReporterMessage, Container)):
			return item
		elif isinstance(item, (list, tuple)):
			return type(item)(cls._hook(elem) for elem in item)
		return item
	
		
	@iclassmethod
	def get_delimiter(self):
		return getattr(self, '_delimiter', ':')
		
		
	#@classmethod
	#def _group(cls, data, field = 'symbol'):
	#	self = cls(data, field='symbol')
	#	return self
	
	#self.fields_list[field] = set(self._grouped.keys())
	#self.field_order.append(field)
	
	def __delitem__(self, key):
		if key in self.mapping:
			del self.mapping[key]
		list.__delitem__(self.data, key)
	
	def insert(self, index, object):
		if isinstance(object, ReporterMessage):
			return list.insert(self.data, index, object)
	
	def __len__(self):
		return len(self.data) + len(self.mapping)
	
	def __setitem__(self, key, value):
		if isinstance(key, int):
			return list.__setitem__(self.data, key, value)
		else:
			self.mapping[key] = value
	
	def __getitem__(self, key):
		#self.mapping[key]
		if isinstance(key, int):
			return list.__getitem__(self.data, key)
		else:
			if key in self.mapping:
				return self.mapping[key]
	
	def __missing__(self, key):
		if key in self.__dict__:
			return self.__dict__[key]
		return None
	
	def __iter__(self):
		return iter(self.data)
	
	
	def keys(self):
		"""Return a copy of the flat dictionary's list of keys.
		See the note for :meth:`flatdict.FlatDict.items`.

		:rtype: list

		"""
		keys = []
		for key, value in self.mapping.items():
			if isinstance(value, (self.__class__, dict)):
				keys += [self._delimiter.join([key, k]) for k in value.keys()]
			else:
				keys.append(key)
		return sorted(keys)

	def iterkeys(self):
		return collections.KeysView(self.mapping)
	
	def itervalues(self):
		return collections.ValuesView(self.mapping)
	
	def iteritems(self):
		return collections.ItemsView(self.mapping)


	def __repr__(self):
		if self.mapping and not self.data:
			items = self.mapping.copy()
		if self.data and not self.mapping:
			items = self.data[:]
		if self.data and self.mapping:
			items = self.data
		if not self.data and not self.mapping:
			items = ()
		#items = ()
		return '{}({!r})'.format(self.__class__.__name__, items)
	
	make_flat_key = make_flat_key
	
	lookup = lookup



delimiter_re = regex.compile(r'[:|/]')

@return_as(list)
def _consecutive_slices(iterable):
	"""Build a list of consecutive slices of a given path.


	>>> list(_consecutive_slices([1, 2, 3]))
	[[1], [1, 2], [1, 2, 3]]
	"""
	return (iterable[:i] for i in range(1, len(iterable) + 1))



def group(data, node, path_limit =[('symbol', 'column')],):
	node = node or []
	grouper = False
	
	key = make_flat_key(node)
	
	if isinstance(data, (MutableMapping,)):
		grouper = True
	
	if isinstance(data, (MutableSequence,)):
		grouper = True



def _groupby(key, seq, **kwargs):
	"""
	
	:param key:
	:param seq:
	:return:
	
	"""
	from collections import defaultdict
	from startups.misc import attrgetter
	
	
	
	fields_list = kwargs.get('fields_list', defaultdict(set))
	field_order = kwargs.get('field_order', list(fields_list))
	
	d = defaultdict(MessageList)
	attr = key[:]
	key = attrgetter(key)
	for item in seq:
		d[key(item)].append(item)
		
		
	fields_list[attr].update(d)
	
	field = attr
	return MessageList(dict(d), fields_list =fields_list, field_order =list(fields_list), field = field)
	
	

@return_as(MessageList)
@return_as(dict)
def grouped(field, dic):
	from startups.misc import attrgetter
	
	if isinstance(dic, dict):
		for k, v in dic.items():
			v = groupby(attrgetter(field), v)
			yield (k,v)
	
	else:
		v = groupby(attrgetter(field), dic)
		yield v





class _MessageList(object):
	_field_names = ReporterMessage._fields
	_delimiter = ':'
	__slots__ = ['__dict__', 'field', 'field_list', 'field_order']
	
	def __init__(self, *args, **kwargs):
		self.data = []
		self.mapping = kwargs.copy()
		self._keys = set([])
		
		for arg in args:
			if not arg:
				continue
			
			elif isinstance(arg, dict):
				for key, val in arg.items():
					self[key] = self._hook(val)
					self._keys.add(key)
			
			elif isinstance(arg, list):
				self.data += arg
			
			elif isinstance(arg, ReporterMessage):
				self.data.append(arg)
		
		#for key, val in kwargs.items():
		#	setattr(self, key, val)
	
	@classmethod
	def _hook(cls, item):
		if isinstance(item, dict):
			return cls(item)
		elif isinstance(item, (ReporterMessage, Container)):
			return item
		
		elif isinstance(item, (list, tuple)):
			return type(item)(cls._hook(elem) for elem in item)
		return item
	
	
	@classmethod
	def _group(cls, data, field):
		self = cls(data)
	
	#self.fields_list[field] = set(self._grouped.keys())
	#self.field_order.append(field)
	
	def __delitem__(self, key):
		if key in self.mapping:
			del self.mapping[key]
		list.__delitem__(self.data, key)
	
	def insert(self, index, object):
		if isinstance(object, ReporterMessage):
			return list.insert(self.data, index, object)
	
	def __len__(self):
		return len(self.data) + len(self.mapping)
	
	def __setitem__(self, key, value):
		if isinstance(key, int):
			return list.__setitem__(self.data, key, value)
		else:
			self.mapping[key] = value
	
	def __getitem__(self, key):
		#self.mapping[key]
		if isinstance(key, int):
			return list.__getitem__(self.data, key)
		else:
			if key in self.mapping:
				return self.mapping[key]
		
	
	def __missing__(self, key):
		if key in self.__dict__:
			return self.__dict__[key]
		return None
	
	def __iter__(self):
		return iter(self.data)
	
	def iterkeys(self):
		return collections.KeysView(self.mapping)
	
	def itervalues(self):
		return collections.ValuesView(self.mapping)
	
	def iteritems(self):
		return collections.ItemsView(self.mapping)
	
	def __repr__(self):
		if self.mapping and not self.data:
			items = self.mapping.copy()
		if self.data and not self.mapping:
			items = self.data[:]
		if self.data and self.mapping:
			items = self.data
		if not self.data and not self.mapping:
			items = ()
		#items = ()
		return '{}({!r})'.format(self.__class__.__name__, items)

class MessageComp(TupleComp):
	def compare_attr(self, left, right):
		for index, direction in self.comp_select_list:
			l = getattr(left, index)
			r = getattr(right, index)
			if l < r:
				return -direction
			if l > r:
				return direction
			return 0



class MessagesSorter(object):
	MESSAGE_FIELDS = MESSAGE_FIELDS
	
	sort_arg_defs = [
		('msg_id', (((0, 1),), 'msg_id')),
		('symbol', (((1, 1),), 'symbol')),
		('msg', (((2, 1),), 'message_text')),
		('C', (((3, 1),), 'category abbreviation')),
		('category', (((4, 1),), 'category')),
		('confidence', (((5, 1),), 'confidence')),
		('abspath', (((6, 1),), 'abspath')),
		('path', (((7, 1),), 'path relative to base')),
		('module', (((8, 1),), 'module')),
		('obj', (((9, 1),), 'object-name')),
		('line', (((10, 1),), 'line number')),
		('column', (((11, 1),), 'column number')),
		('order', (((6, 1), (10, 1), (11, 1)), 'abspath:lineno:column')),
		('checker', (((12, 1),), 'checker name')),
		('fullname', (((13, 1),), 'module:object-name')), ]
	
	sort_arg_defs_defaults = OrderedDict(sort_arg_defs)
	
	def __init__(self, reporter, **kwargs):
		self.reporter = reporter
		
		self.linter = getattr(self.reporter, 'linter', None)
		
		if hasattr(self.reporter, 'msgs'):
			self.msgs = self.reporter.msgs.copy()
		elif hasattr(self.reporter, 'messages'):
			self.msgs = self.reporter.messages.copy()
		else:
			self.msgs = []
			
		self.msgs_list = []
		
		for key, val in kwargs.items():
			setattr(self, key, val)
	
	def set_linter(self, linter):
		self.linter = linter
	
	def get_sort_arg_defs(self):
		try:
			return dict(self.sort_arg_defs)
		except (TypeError, ValueError):
			results = dict()
			for name, sort_tuple, sort_type in self.sort_arg_defs:
				results[name] = (sort_tuple, sort_type)
			return results
	
	def sort_messages(self, *field):
		"""

		#sort(key=cmp_to_key(TupleComp(sort_tuple).compare))

		:return:
		"""
		from functools import cmp_to_key
		
		sort_arg_defs = self.sort_arg_defs_defaults
		sort_tuple = ()
		self.sort_type = ""
		connector = ""
		for word in field:
			sort_tuple = sort_tuple + sort_arg_defs[word][0]
			self.sort_type += connector + sort_arg_defs[word][1]
			connector = ", "
		
		self.sort_tuple = sort_tuple
		msgs_list = []
		#self.msgs_list
		for m in self.msgs:
			#item = m._asdict()
			
			msgs_list.append(tuple(m))
		
		msgs_list.sort(key=cmp_to_key(TupleComp(sort_tuple).compare)) #change
		
		self.sort_key = cmp_to_key(TupleComp(sort_tuple).compare)
		self.msgs_list = msgs_list
		print(self.sort_type)
		return self.sort_key
	
	
	def group(self, field, dic):
		from startups.misc import attrgetter
		if isinstance(dic, dict):
			for k,v in dic.items():
				v = groupby(attrgetter(field), v)
		else:
			v = groupby(attrgetter(field), dic)
		return v
		
	
	def groupby(self, key, seq):
		from collections import defaultdict
		from startups.misc import attrgetter
		d = defaultdict(list)
		key = attrgetter(key)
		for item in seq:
			d[key(item)].append(item)
		return d
	
	
	def grouped(self, *fields): #TODO!!!!
		"""
		
		:param fields:
		:return:
		TODO check it is being passed `ReporterMessage`
		"""
		#fields_list = self.fields_list = fields
		from toolz import groupby
		from startups.misc import attrgetter
		from collections import defaultdict
		self.fields_list = defaultdict(set)
		self.field_order = []
		
		for field in fields:
			if not self.fields_list:
				self._grouped = groupby(attrgetter(field), self.msgs)
				
				self.fields_list[field] = set(self._grouped.keys())
				self.field_order.append(field)
			
			else:
				for order in self.field_order:
					for key in self.fields_list[order]:
						if self._grouped.get(key):
							print(key)
							srt = self._grouped[key]
							srt = self.group(field, srt)
							self._grouped[key] = srt
						#print(self._grouped[key])
						#self._grouped[key] = groupby(attrgetter(field), self._grouped[key])
						for subfield in self._grouped.get(key):
							self.fields_list[field].add(subfield)
				self.field_order.append(field)
				
				
				#for k, v in self._grouped.items():
			#pylint.utils.get_module_and_frameid
				#
				#	grpkey = self._grouped[k]
				#
				#	self._grouped[k] = groupby(attrgetter(field), self._grouped[k])
				#	print(k, len(self._grouped[k]))
				#	for subfield in self._grouped[k]:
				#		self.fields_list[field].add(subfield)
				
				
				#for name in self.fields_list[-1:]:
				#	print(name, self.fields_list.index(name))
				#for k,v in self._grouped.items():
				#
				#	self._grouped = groupby(attrgetter(field), self.msgs)
					
		return self._grouped
	
	def get_msg_checker_name(self, msg): #TODO not needed?
		if not self.linter:
			return
		store = self.linter.msgs_store
		desc = msg.symbol
		return store.check_message_id(msg.symbol).checker.name
	
	def get_msg_fullname(self, msg):
		return '.'.join([msg.module, msg.obj]).strip('.')
	
	def get_print_list(self, sel_list): #TODO from pstats!
		pass
	
	def eval_print_amount(self, sel, lst, msg):
		pass
###



def _get_example_data():
	"""
	
	:return:
	
	>>> m = _get_example_data()
	>>> bool(m)
	True
	
	"""
	from startups.core import unpickler
	EXAMPLE_DATA = '/Users/kristen/PycharmProjects/LINTFUL_REPORTER_EXAMPLE.pkl'
	return unpickler(EXAMPLE_DATA)

EX = _get_example_data()



if __name__ == '__main__':
	
	from doctest import testmod
	testmod(__self__, verbose = 2)
