#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = handlers
# author=KGerring
# date = 3/16/18
# from startups import *
"""

"""

from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

#durable = True, routing_key = ''
#Connection('amqp://guest:guest@localhost:5672//') #conn.release()

#headers

@__all__.add
class BaseHandler(object):
	properties = dict()
	headers = dict()
	
	def send(self, message):
		pass
	
	def recieve(self):
		pass
	
#self.options[-1][1]['callback'](option, opt, val, p, level=1)



#L.load_default_plugins

	

if __name__ == '__main__': print(__file__)


