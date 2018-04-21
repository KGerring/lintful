#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['token_column_distance', 'TokenWrapper', 'Stats']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__
import tokenize
#from pylint.checkers.format import _column_distance as token_column_distance

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseTokenChecker
import six
from pylint.checkers.format import TokenWrapper as _TokenWrapper

from startups.core import pickler, unpickler
from collections import MutableMapping
from pylint.config import _get_pdata_path, load_results, save_results
from addict import Dict
from startups.core import SliceableDict


USES = ['lintful.plugins.base.ReporterMessage','pylint.utils._MsgBase','pylint.utils.Message']


class Stats(MutableMapping):
	"""
	A class meant to load `stats` from a filename or with a mapping; or blank-mapping
	"""
	PYLINTHOME = os.environ.get('PYLINTHOME')
	suffix = 1
	ext = '.stats'
	
	def __init__(self, *args, **kwargs):
		"""
		
		:param dict args: A mapping to initialize with
		:param str kwargs: accepts `filename` as a filename to load with; also `suffix`
		"""
		
		if args:
			if len(args) == 1:
				self.data = args[0]
				self.update(self.data)
			elif len(args) == 2:
				self.data, filename = args
				self.update(self.data)
				self.filename = filename
			elif len(args) == 3:
				self.data, filename, suffix = args
				self.update(self.data)
				self.filename = filename
				self.suffix = suffix
				
		if not args:
			self.data = dict()
			self.update(self.data)
			filename = None
			self.filename = filename
			
		for k,v in kwargs.items():
			setattr(self, k, v)
			
		if 'filename' in kwargs:
			file = kwargs.get('filename')
			self.load_data(file)
	
	
	@classmethod
	def from_file(cls, filename):
		"""
		Load a Stats from an abspath filename
		:param str filename:
		:return:
		"""
		self = cls()
		self.load_data(filename)
		return self
		
	
	
	def load_data(self, filename, suffix = None):
		"""
		Load the data from an abspath `filename` or with a base-name and suffix
		:param filename:
		:param int suffix: default is 1; A number for the recurs for `pylint.config._get_pdata_path`
		:return: The `Stats` class instance with data loaded
		"""
		if not suffix:
			suffix = self.suffix
			
		if not filename.startswith(self.PYLINTHOME):
			filename = _get_pdata_path(filename, suffix)
			
		self.data = unpickler(filename)
		self.filename = filename
		return self
	
	def dump_data(self, filename = None, suffix = 1):
		"""
		Dump the data to a filename. If a filename isnt an abspath then deduce it with suffix
		:param str filename: An abspath or a base-name
		:param int suffix: A number for the recurs for `pylint.config._get_pdata_path`; default = 1
		:return:
		"""
		if not filename:
			filename = self.filename
		if not filename.startswith(self.PYLINTHOME):
			filename = _get_pdata_path(filename, suffix)
		pickler(self.data, filename)
		return filename
	
			
	def fileinfo(self, filename):
		dirname, basename = os.path.split(filename)
		base, ext = os.path.splitext(basename)
		try:
			self.suffix = int(base[-1:])
		except TypeError:
			pass
		self.basename = base[:-1]
		
	def inc_suffix(self):
		self.suffix +=1
	
		return '{}{}{}'.format(self.basename, self.suffix, self.ext)
	
	def __missing__(self, key):
		if key in self.__dict__:
			return self.__dict__[key]
		return None
	
	def __len__(self): return len(self.data)
	
	def __getitem__(self, key):
		if key in self.data:
			return self.data[key]
		if hasattr(self.__class__, "__missing__"):
			return self.__class__.__missing__(self, key)
		raise KeyError(key)
	
	def __setitem__(self, key, item):
		self.data[key] = item
	
	def __delitem__(self, key): del self.data[key]
	
	def __iter__(self):
		return iter(self.data)
	
	def __contains__(self, key):
		return key in self.data
	
	def __repr__(self): return repr(self.data)
	
	def copy(self):
		if self.__class__ is Stats:
			return Stats(self.data.copy())
		import copy
		
		data = self.data
		try:
			self.data = {}
			c = copy.copy(self)
		finally:
			self.data = data
		c.update(self)
		return c
	
	@classmethod
	def fromkeys(cls, iterable, value=None):
		d = cls()
		for key in iterable:
			d[key] = value
		return d


class PylintStats(Stats):
	
	PYLINTHOME = os.environ.get('PYLINTHOME')
	_re = regex.compile(r'.*(\d)\.\w+$')
	
	#def __init__(self, filename = None):
	#	self.filename = filename or ''
	#	self.relpath = os.path.relpath(self.filename, self.PYLINTHOME)
	#	self.basename = os.path.splitext(self.relpath)[0]
	#	self.suffix = int(self.basename[-1:])
	#	self.basename = self.basename[:-1]
	#
	
	#def load_file(self, filename):
	#	return unpickler(filename)
	
	def dump_file(self, filename):
		return pickler(self, filename)
	
	def __getattr__(self, k):
		""" Gets key if it exists, otherwise throws AttributeError.

			nb. __getattr__ is only called if key is not found in normal places.

			>>> b = PylintStats(bar='baz')
			>>> b.foo
			Traceback (most recent call last):
				...
			AttributeError: foo

			>>> b.bar
			'baz'
			>>> getattr(b, 'bar')
			'baz'
			>>> b['bar']
			'baz'

			#>>> b.lol is b['lol']
			#True
			#>>> b.lol is getattr(b, 'lol')
			#True
		"""
		k = k.replace('-', '_')
		try:
			# Throws exception if not in prototype chain
			return object.__getattribute__(self, k)
		except AttributeError:
			try:
				return self[k]
			except KeyError:
				raise AttributeError(k)
	
	#def __setattr__(self, k, v):
	#	try:
	#		# Throws exception if not in prototype chain
	#		object.__getattribute__(self, k)
	#	except AttributeError:
	#		try:
	#			self[k] = v
	#		except:
	#			raise AttributeError(k)
	#	else:
	#		object.__setattr__(self, k, v)
			



def dictify(x,factory=PylintStats):
	if isinstance(x, dict):
		return factory((k, dictify(v, factory)) for k, v in x.items())
	
	elif isinstance(x, (list, tuple)):
		return type(x)(dictify(v, factory) for v in x)
	else:
		return x
del dictify

def relative_path(path):
	"""
	Get a relative-path from the available paths in sys.path
	:param str path:
	:return: A relative path for path
	"""
	comparepath = os.path.normcase(path)
	longest = ""
	for _dir in sys.path:
		_dir = os.path.normcase(_dir)
		if comparepath.startswith(_dir) and comparepath[len(_dir)] == os.sep:
			if len(_dir) > len(longest):
				longest = _dir
	
	if longest:
		base = path[len(longest) + 1:]
	else:
		base = path
	
	drive, base = os.path.splitdrive(base)
	if os.altsep:
		base = base.replace(os.altsep, ".")
	return base



#R._asdict()
#UserDict,ChainMap

from collections import MutableMapping, MutableSequence, _Link, _proxy, ChainMap




class Link(object):
	__slots__ = 'prev', 'next', 'key', '__weakref__'
	
	def __repr__(self):
		if hasattr(self, 'key'):
			return '{}(key={!r})'.format('Link', self.key)
		else:
			return 'Link at {:#x}'.format(id(self))








class TokenWrapper(_TokenWrapper):
	
	def end_col(self, idx):
		return self._tokens[idx][3][1]
	
	def end_line(self, idx):
		return self._tokens[idx][3][0]

def tokenize_node(ast_node,):
	from pylint.checkers.format import TokenWrapper
	from pylint.utils import tokenize_module
	tokens = tokenize_module(ast_node)
	return TokenWrapper(tokens)

def untokenize_node(tokens, L = None):
	import astroid
	file_bytes = tokenize.untokenize(tokens).decode()
	from astroid.builder import AstroidBuilder
	Builder = AstroidBuilder(astroid.MANAGER)
	
del tokenize_node, untokenize_node
del TokenWrapper




if __name__ == '__main__': print(__file__)