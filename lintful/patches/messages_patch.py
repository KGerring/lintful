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
#from functools import wraps

#config.register_options_provider
#config.load_provider_defaults
#config.load_defaults.742
#utils.category_id (136)
#utils.register_report,enable_report,register_plugins
#pylint.interfaces.implements
#reporters.set_output (62)
#reporters.initialize (131)
#pylint.lint.register_reporter      679 8
#pylint.lint.register_checker      696 33
#pylint.checkers.refactoring._init  153


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









if __name__ == '__main__': print(__file__)