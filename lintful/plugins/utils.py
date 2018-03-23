#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = utils
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['token_column_distance', 'TokenWrapper']
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