#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = reports
# author= KGerring
# date = 3/28/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = ['ReportWriter', 'JSONWriter', 'HTMLWriter', 'reduce_sections', 'from_dot']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import pylint
import pylint.reporters

from pylint.reporters.ureports.text_writer import TextWriter
try:
	import pylint.reporters.ureports.nodes as reportnodes
except AttributeError:
	reportnodes = sys.modules['pylint.reporters.ureports.nodes']

from decorator import dispatch_on
from startups.core import ignore_parameterize
from startups.misc import attrgetter
from pygraphviz.agraph import AGraph
from networkx import DiGraph
#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__



def from_dot(filename, strict = True, directed = True, string = None):
	"""
	
	:param filename:
	:param strict:
	:param directed:
	:param string:
	:return:
	"""
	
	A = AGraph(directed = directed, strict = strict)
	with open(filename) as reader:
		data = reader.read()
	A.from_string(data)
	return A
	#layout
	
	#from_string




def nx_to_json_graph(digraph, inline = True):
	from networkx.readwrite import node_link_data
	data = node_link_data(digraph, {'link': 'edges', 'source': 'from', 'target': 'to'})
	if inline:
		digraph['node_link_data'] = data
		return digraph
	else:
		return data


def int_dependencies_from_stats(linter_checker):
	import six
	package = self.linter.current_name
	__int_dep_info = result = {}
	for importee, importers in six.iteritems(self.stats['dependencies']):
		if importee.startswith(package):
			result[importee] = importers
	__int_dep_info


def ext_dependencies_from_stats(linter_checker):
	import six
	
	package = self.linter.current_name
	__ext_dep_info = result = {}
	for importee, importers in six.iteritems(self.stats['dependencies']):
		if not importee.startswith(package):
			result[importee] = importers


def get_evaluation(linter):  #TODO add to linter
	self = linter
	from pylint import config
	
	previous_stats = config.load_results(self.file_state.base_name)
	if self.stats['statement'] == 0:
		return
	evaluation = self.config.evaluation
	try:
		note = eval(evaluation, {}, self.stats) # pylint: disable=eval-used
	except Exception as ex: # pylint: disable=broad-except
		note = 'NA'
	
	pnote = previous_stats.get('global_note', None)
	if not pnote:
		if previous_stats.get('statement', 0) == 0:
			pnote = 'NA'
		else:
			try:
				pnote = eval(evaluation, {}, previous_stats)
			except Exception as ex:
				pnote = 'NA'
	if isinstance(note, (int, float)) and isinstance(pnote, (int, float)):
		dnote = note - pnote
	else:
		dnote = 'NA'
	
	results = list(zip(
			['stats', 'previous_stats', 'difference'],
			(note, pnote, dnote)))
	return {"evaluation": results}


def reduce_sections(sect):
	"""
	Return the table-nodes from the Section
	:param sect: A `Section` instance
	:return: A list of `Table` nodes
	"""
	import collections
	
	node = collections.deque(sect)
	items = []
	while node:
		item = node.popleft()
		visitname = item._get_visit_name()
		if visitname == 'table':
			items.append(item)
		
		elif visitname in ('paragraph', 'title',
		                   'text', 'evaluationsection', 'verbatimtext'):
			items.append(item)
		
		elif visitname == 'section':
			node.extend(list(item))
		else:
			node.extend(list(item))
	return items

class ReportWriter(TextWriter):
	out = sys.stdout
	section = 0
	list_level = 0

	@dispatch_on('layout')
	def dump(self, layout):
		return layout
	
	
	@dump.register(reportnodes.Text)
	
	def dump_text(self, layout):
		return layout.data
	
	@dump.register(reportnodes.VerbatimText)
	def dump_verbatimtext(self, layout):
		return layout.data.splitlines()
	#@dump.register(reportnodes.Section)
	#def dump_orig_section(self, layout):
	#	return layout
	
	@dump.register(reportnodes.Paragraph)
	def dump_paragraph(self, layout):
		return ignore_parameterize(''.join(list(self.compute_content(layout))), ' ')
	
	@dump.register(reportnodes.Title)
	def dump_title(self, layout):
		return ignore_parameterize(''.join(list(self.compute_content(layout))), '_').upper()
	
	@dump.register(reportnodes.Table)
	def dump_table(self, layout):      #TOD pythonize, startups.core.ignore_parameterize('%')
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
		
		return [self.dump(child) for child in getattr(layout, 'children', ())]
		
		
	@dump.register(reportnodes.Section)
	def dump_two_section(self, layout):
		children = getattr(layout, 'children', ())
		if len(children) == 2:
			title = self.dump(children[0])
			table = self.dump(children[1])
			return {title:table}
		else:
			return [self.dump(child) for child in children]
		
		#for child in getattr(layout, 'children', ()):
		#	self.dump(child)
	#
		#	#child.accept(self)


class HTMLWriter(TextWriter):
	"""format layouts as HTML"""
	out = sys.stdout
	section = 0
	list_level = 0
	
	def __init__(self, snippet=None):
		super(HTMLWriter, self).__init__()
		self.snippet = snippet
		
		
	def format(self, layout, stream=None, encoding=None):
		if stream is None:
			stream = sys.stdout
		if not encoding:
			encoding = getattr(stream, 'encoding', 'UTF-8')
		self.encoding = encoding or 'UTF-8'
		self.out = stream
		if self.snippet is None:
			self.writeln(u'<html>')
			self.writeln(u'<body>')
		layout.accept(self)
		if self.snippet is None:
			self.writeln(u'</body>')
			self.writeln(u'</html>')
	
	def handle_attrs(self, layout):
		"""get an attribute string from layout member attributes"""
		from operator import methodcaller
		
		klassname = methodcaller('_get_visit_name')
		
		attrs = u''
		#klass = getattr(layout, 'klass', None)
		klass = klassname(layout) or None
		if klass:
			attrs += u' class="%s"' % klass
		nid = getattr(layout, 'report_id', None)
		if nid:
			attrs += u' id="%s"' % nid
		return attrs
	
	
	
	def begin_format(self, layout):
		"""begin to format a layout"""
		super(HTMLWriter, self).begin_format(layout)
		if self.snippet is None:
			self.writeln(u'<html>')
			self.writeln(u'<body>')
	
	def end_format(self, layout):
		"""finished to format a layout"""
		if self.snippet is None:
			self.writeln(u'</body>')
			self.writeln(u'</html>')
	
	def visit_section(self, layout):
		"""display a section as html, using div + h[section level]"""
		self.section += 1
		self.writeln(u'<div%s>' % self.handle_attrs(layout))
		self.format_children(layout)
		self.writeln(u'</div>')
		self.section -= 1
	
	def visit_title(self, layout):
		"""display a title using <hX>"""
		self.write(u'<h%s%s>' % (self.section, self.handle_attrs(layout)))
		self.format_children(layout)
		self.writeln(u'</h%s>' % self.section)
	
	def visit_table(self, layout):
		"""display a table as html"""
		self.writeln(u'<table%s>' % self.handle_attrs(layout))
		table_content = self.get_table_content(layout)
		for i in range(len(table_content)):
			row = table_content[i]
			if i == 0 and layout.rheaders:
				self.writeln(u'<tr class="header">')
			elif i + 1 == len(table_content):# and layout.rrheaders:
				self.writeln(u'<tr class="header">')
			else:
				self.writeln(u'<tr class="%s">' % (i % 2 and 'even' or 'odd'))
			for j in range(len(row)):
				cell = row[j] or u'&#160;'
				if (layout.rheaders and i == 0) or \
						(layout.cheaders and j == 0) :#or \
						#(layout.rrheaders and i + 1 == len(table_content)) or \
						#(layout.rcheaders and j + 1 == len(row)):
					self.writeln(u'<th>%s</th>' % cell)
				else:
					self.writeln(u'<td>%s</td>' % cell)
			self.writeln(u'</tr>')
		self.writeln(u'</table>')
	
	def visit_list(self, layout):
		"""display a list as html"""
		self.writeln(u'<ul%s>' % self.handle_attrs(layout))
		for row in list(self.compute_content(layout)):
			self.writeln(u'<li>%s</li>' % row)
		self.writeln(u'</ul>')
	
	def visit_paragraph(self, layout):
		"""display links (using <p>)"""
		self.write(u'<p>')
		self.format_children(layout)
		self.write(u'</p>')
	
	def visit_span(self, layout):
		"""display links (using <p>)"""
		self.write(u'<span%s>' % self.handle_attrs(layout))
		self.format_children(layout)
		self.write(u'</span>')
	
	def visit_link(self, layout):
		"""display links (using <a>)"""
		self.write(u' <a href="%s"%s>%s</a>' % (layout.url,
		                                        self.handle_attrs(layout),
		                                        layout.label))
	
	def visit_verbatimtext(self, layout):
		"""display verbatim text (using <pre>)"""
		self.write(u'<pre>')
		self.write(layout.data.replace(u'&', u'&amp;').replace(u'<', u'&lt;'))
		self.write(u'</pre>')
	
	def visit_text(self, layout):
		"""add some text"""
		data = layout.data
		if layout.escaped:
			data = data.replace(u'&', u'&amp;').replace(u'<', u'&lt;')
		self.write(data)


class JSONWriter(TextWriter):
	out = sys.stdout
	section = 0
	list_level = 0
	
	def set_output(self, out=sys.stdout):
		setattr(self, 'out', out)
	
	def begin_format(self):
		super(TextWriter, self).begin_format()
		self.list_level = 0
	
	#'%documented', '%badname'      #TOD regex for this!!!
	
	
	#layout.accept(self)
	
	
	def visit_table(self, layout):      #TOD pythonize, startups.core.ignore_parameterize('%')
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
	
	def visit_title(self, layout):
		return startups.core.ignore_parameterize(''.join(list(self.compute_content(layout))
		                                                 ), '_').upper()
	
	def visit_paragraph(self, layout):
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