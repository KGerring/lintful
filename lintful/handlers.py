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
#lintful.plugins.base.ReporterMessage
#logbook.LogRecord, FileHandler

#durable = True, routing_key = ''
#Connection('amqp://guest:guest@localhost:5672//') #conn.release()
import dictdiffer

BACKENDS = ['couchdb'] #TODO find?

from logbook.base import LogRecord

#message        #kwargs
class RecordMessage(LogRecord):
	
	def format(self, msg, *args, **kwargs):
		return self._format_message(msg, *args, **kwargs)
	
	#stack_manager
	#self._formatter.format(record=record, handler=handler)

@__all__.add
class BaseHandler(object):
	properties = dict()
	headers = dict()
	
	def send(self, message):
		pass
	
	def recieve(self):
		pass

"""
from datetime import datetime
from couchdb.mapping import (Document, TextField, IntegerField, DateTimeField, DictField, Field, ListField, Mapping)

class MessageDocument(Document):
	msg_id = TextField()
	symbol = TextField()
	msg = TextField()
	C = TextField()
	category = TextField()
	confidence = TextField()
	abspath = TextField()
	path = TextField()
	module = TextField()
	obj = TextField()
	line = IntegerField()
	column = IntegerField()
	

class MessagesDocument(Document):
	""""""
	abspath = TextField()
	date = DateTimeField(default=datetime.now)
	messages = ListField(DictField(Mapping.build(
		msg_id=TextField(),
		symbol = TextField(),
		msg = TextField(),
		C = TextField(),
		category = TextField(),
		confidence = TextField(),
		abspath = TextField(),
		path = TextField(),
		module = TextField(),
		obj = TextField(),
		line = IntegerField(),
		column = IntegerField(),
	)))
	

"""



	
#logbook.FileHandler
#'http://localhost:5984/lintful'



#L.load_default_plugins
#mimetypes.MimeTypes
#http://localhost:5984/lintful/_all_docs
#'http://localhost:5984/lintful/{}'.format(did)

COUCHDB_VIEWS = """function(doc) {
  emit(null, doc);
}

function(doc) {
  emit([doc._id], doc._attachments);
}



view = ViewDefinition('tests', 'all', '''function(doc) {
     emit(doc._id, null);
 }''')
 view.get_doc(db)


view.sync(db)
design_doc = view.get_doc(db)

print(design_doc['views']['all']['map'])


###
 def my_map(doc):
     yield doc['_id']
     
v = ViewDefinition('test2', 'somename', my_map, language='python')

"""


if __name__ == '__main__': print(__file__)


