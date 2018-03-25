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
from pylint.checkers.format import TokenWrapper, _column_distance as token_column_distance

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseTokenChecker
import six
from pylint.checkers.format import TokenWrapper as _TokenWrapper

from startups.core import pickler, unpickler
from collections import MutableMapping
from pylint.config import _get_pdata_path, load_results, save_results
from addict import Dict



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


def relative_path(path):
	"""
	Get a relative-path from the available paths in sys.path
	:param str path:
	:return: A relative path for path
	"""
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
	#Builder.string_build(L.current_name, L.current_file)
	#_parse
	
	#self = linter
	#self.process_tokens(tokens)
	#self.file_state.collect_block_lines(self.msgs_store, ast_node)
	#
	#orig_state = self._module_msgs_state.copy()
	#self._module_msgs_state = {}
	#self._suppression_mapping = {}
	##self._collect_block_lines(msgs_store, ast_node, orig_state)


#def _collect_block_lines(self, msgs_store, node, msg_state):
#	"""Recursively walk (depth first) AST to collect block level options
#	line numbers.
#	"""
#	from astroid import nodes
#	import six
#	from pylint.utils import WarningNode
#
#	#self.msgs_store
#
#	for child in node.get_children():
#		self._collect_block_lines(msgs_store, child, msg_state)
#	first = node.fromlineno
#	last = node.tolineno
#	# first child line number used to distinguish between disable
#	# which are the first child of scoped node with those defined later.
#	# For instance in the code below:
#	#
#	# 1.   def meth8(self):
#	# 2.        """test late disabling"""
#	# 3.        # pylint: disable=E1102
#	# 4.        print self.blip
#	# 5.        # pylint: disable=E1101
#	# 6.        print self.bla
#	#
#	# E1102 should be disabled from line 1 to 6 while E1101 from line 5 to 6
#	#
#	# this is necessary to disable locally messages applying to class /
#	# function using their fromlineno
#	if (isinstance(node, (nodes.Module, nodes.ClassDef, nodes.FunctionDef))
#	    and node.body):
#		firstchildlineno = node.body[0].fromlineno
#	else:
#		firstchildlineno = last
#	for msgid, lines in six.iteritems(msg_state):
#		for lineno, state in list(lines.items()):
#			original_lineno = lineno
#			if first > lineno or last < lineno:
#				continue
#			# Set state for all lines for this block, if the
#			# warning is applied to nodes.
#			if msgs_store.check_message_id(msgid).scope == WarningScope.NODE:
#				if lineno > firstchildlineno:
#					state = True
#				first_, last_ = node.block_range(lineno)
#			else:
#				first_ = lineno
#				last_ = last
#			for line in range(first_, last_ + 1):
#				# do not override existing entries
#				if line in self._module_msgs_state.get(msgid, ()):
#					continue
#				if line in lines: # state change in the same block
#					state = lines[line]
#					original_lineno = line
#				if not state:
#					self._suppression_mapping[(msgid, line)] = original_lineno
#				try:
#					self._module_msgs_state[msgid][line] = state
#				except KeyError:
#					self._module_msgs_state[msgid] = {line: state}
#			del lines[lineno]




if __name__ == '__main__': print(__file__)