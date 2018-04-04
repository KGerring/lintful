#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = messages_patch
# author= KGerring
# date = 4/3/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from pylint.utils import MessagesHandlerMixIn, UNDEFINED
from pylint.lint import PyLinter


def patch_messages():
	"""Patch MessagesHandlerMixIn to pass the node to reporter."""
	old_add_message = MessagesHandlerMixIn.add_message
	
	def new_add_message(self, msg_descr, line=None, node=None, args=None,
	                    confidence=UNDEFINED):
		old_add_message(self, msg_descr, line, node, args, confidence)
		msg_info = self.msgs_store.check_message_id(msg_descr)
		self.reporter.handle_node(msg_info, node)
	
	MessagesHandlerMixIn.add_message = new_add_message

def patch_add_message():
	old = getattr(MessagesHandlerMixIn, "add_message")
	

#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

def add_messages():
	old_add_message = getattr(MessagesHandlerMixIn, "add_message")
	def new_add_message(self, *args, **kwargs):
		old_add_message(self, *args, **kwargs)
		msg_descr = args[1] or kwargs.get('msg_descr')
		msg_info = self.msgs_store.check_message_id(msg_descr)
		self.reporter.handle_node(msg_info, node)


from functools import wraps







if __name__ == '__main__': print(__file__)