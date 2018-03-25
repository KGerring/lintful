#!/usr/bin/env
# -*- coding: utf-8 -*-
# filename = serializers
# author=KGerring
# date = 3/16/18
# from startups import *
"""

"""

from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = ['ExternalDependenciesGraph', 'make_tree_defs', 'string_tree_defs', 'get_tables']
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip

from lintplus.plugins.reporters import get_evaluation, dependencies_graph, get_json_graph, JSONWriter
from pylint.reporters.ureports.text_writer import TextWriter, BaseWriter
from importpy.refactoring.pylint_checkers import get_tables, path_time
from path import Path
from pylint.lint import _merge_stats
from pylint.config import load_results, _get_pdata_path
from importpy.refactoring.config import JSONSerializer

from pylint.reporters.ureports.nodes import (BaseLayout, EvaluationSection, Paragraph, Section, Table, Text, Title, VNode, VerbatimText)

from lintplus.py_lint import ExternalDependenciesGraph, make_tree_defs, string_tree_defs
from importpy.refactoring.pylint_checkers import get_tables
#from pylint.config import Option, OptionParser, ConfigurationMixIn
#UNUSED = L.args['importpy.refactoring._pylint']['unused-import']
#importpy.refactoring.config.dependencies_graph
#config.graph



from startups.helpers.decorators import ExportsList
__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__



@__all__.add
def get_graphviz_source(filename, directory=None, format='dot', engine='dot'):
	from graphviz.files import Source
	
	src = Source.from_file(filename, directory=directory,
	                        format=format, engine=engine)
	src.filename = filename[:-4]
	return src



@__all__.add
def run_dot(outputfile):
	dotfile = outputfile
	import subprocess
	from pylint.graph import target_info_from_filename
	
	renderer = 'dot'
	renderer_exec = subprocess.getoutput('which dot')
	storedir, _, target = target_info_from_filename(outputfile)
	dot_sourcepath = os.path.join(storedir, dotfile)
	subprocess.call([renderer_exec, '-T', target,
	                 dot_sourcepath, '-o', outputfile],
	                shell=True)


def reduce_tables(sect):
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
		
		elif visitname in ('paragraph', 'title', 'text'):
			pass
		
		elif visitname == 'section':
			node.extend(list(item))
		else:
			node.extend(list(item))
	
	return items


if __name__ == '__main__': print(__file__)


