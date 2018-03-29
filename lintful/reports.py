#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = reports
# author= KGerring
# date = 3/28/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip




__all__ = ['ReportWriter', 'JSONWriter']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from pylint.reporters.ureports.text_writer import TextWriter
import pylint.reporters.ureports.nodes as reportnodes
from decorator import dispatch_on
from startups.core import ignore_parameterize
from startups.misc import attrgetter

#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


class ReportWriter(TextWriter):
	out = sys.stdout
	section = 0
	list_level = 0

	@dispatch_on('layout')
	def dump(self, layout):
		return layout
	
	@dump.register(reportnodes.Table)
	def dump_table(self, layout):
		return layout
	
	@dump.register(reportnodes.Paragraph)
	def dump_paragraph(self, layout):
		return ignore_parameterize(''.join(list(self.compute_content(layout))), '_').upper()
	
	@dump.register(reportnodes.Title)
	def dump_title(self, layout):
		return ignore_parameterize(''.join(list(self.compute_content(layout))), '_').upper()
	
	@dump.register(reportnodes.Table)
	def dump_table(self, layout):      #TODO pythonize, startups.core.ignore_parameterize('%')
		row_names = None
		report_id = attrgetter('parent.report_id', default='')(layout)
		titleset = set(layout.parent) - set([layout])
		if titleset and len(titleset) == 1:
			title = titleset.pop()
		table_content = self.get_table_content(layout)
		cols = layout.cols
		if layout.rheaders:
			header_row = table_content.pop(0)
		if layout.cheaders:
			row_names = [row[0][:] for row in table_content]
			header_row.pop(0)
		result = []
		for row in table_content:
			if layout.cheaders:
				row_name = row.pop(0)
				jrow = dict(zip(header_row, row))
				drow = {row_name: jrow}
				result.append(drow)
			else:
				jrow = list(zip(header_row, row))
				result.append(jrow)
				
		return result

	@dump.register(reportnodes.Section)
	def dump_section(self, layout):
		for child in layout.children:
			self.dump(child)



class JSONWriter(TextWriter):
	out = sys.stdout
	section = 0
	list_level = 0
	
	def set_output(self, out=sys.stdout):
		setattr(self, 'out', out)
	
	def begin_format(self):
		super(TextWriter, self).begin_format()
		self.list_level = 0
	
	#'%documented', '%badname'      #TODO regex for this!!!
	
	def visit_table(self, layout):      #TODO pythonize, startups.core.ignore_parameterize('%')
		row_names = None
		report_id = attrgetter('parent.report_id', default='')(layout)
		titleset = set(layout.parent) - set([layout])
		if titleset and len(titleset) == 1:
			title = titleset.pop()
		table_content = self.get_table_content(layout)
		cols = layout.cols
		if layout.rheaders:
			header_row = table_content.pop(0)
		if layout.cheaders:
			row_names = [row[0][:] for row in table_content]
			header_row.pop(0)
		result = []
		for row in table_content:
			if layout.cheaders:
				row_name = row.pop(0)
				jrow = dict(zip(header_row, row))
				drow = {row_name: jrow}
				result.append(drow)
			else:
				jrow = list(zip(header_row, row))
				result.append(jrow)
		return {report_id: result}
	
	def _visit_title(self, layout):
		return startups.core.ignore_parameterize(''.join(list(self.compute_content(layout))
		                                                 ), '_').upper()
	
	def _visit_paragraph(self, layout):
		return startups.core.ignore_parameterize(''.join(list(self.compute_content(layout))
		                                                 ), ' ')
	
	def writeln(self, string=u''):
		"""write a line in the output buffer"""
		self.write(string + os.linesep)
	
	def write(self, string):
		"""write a string in the output buffer"""
		self.out.write(string)
		self.out.flush
	
	def write_json(self, mapping):
		self.write(json.dumps(mapping))
		self.out.flush
		self.writeln()
	
	def write_yaml(self, mapping):
		import yaml
		
		self.write(yaml.safe_dump(mapping, default_flow_style=False, canonical=False, indent=4))


if __name__ == '__main__': print(__file__)