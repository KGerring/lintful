#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = checkers_patch
# author= KGerring
# date = 4/3/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip

__all__ = []
import sys # isort:skip
import os # isort:skip
from pylint.checkers.imports import ImportsChecker, _dependencies_graph, _make_graph


def patch_checkers():
	_override_check_reimport()
	_override_report_dependencies_graph()



def _override_check_reimport():
	"""
	
	:return:
	"""
	old_check_reimport = ImportsChecker._check_reimport
	
	def new_check_reimport(node, basename=None, level=None):
		"""check if the import is necessary (i.e. not already done)"""
		from pylint.checkers.imports import _get_first_import
		frame = node.frame()
		root = node.root()
		contexts = [(frame, level)]
		if root is not frame:
			contexts.append((root, None))
		
		for known_context, known_level in contexts:
			for name, alias in node.names:
				first = _get_first_import(
						node, known_context,
						name, basename,
						known_level, alias)
				if first is not None and frame.type not in ('class', 'function'):
					self.add_message('reimported', node=node, args=(name, first.fromlineno))
		
	ImportsChecker._check_reimport = new_check_reimport
	
	#IC._check_reimport = new_check_reimport
	
def _override_report_dependencies_graph():
	
	old_report_dependencies_graph = ImportsChecker._report_dependencies_graph
	
	def new_report_dependencies_graph(self, sect, _, _dummy):
		dep_info = self.stats['dependencies']
		if not dep_info or not (self.config.import_graph
		                        or self.config.ext_import_graph
		                        or self.config.int_import_graph):
			raise EmptyReportError()
		basename = self.linter.current_name
		
		import_graph_filename = self.config.import_graph
		if import_graph_filename:
			
			filename = '{}.{}'.format(basename, import_graph_filename)
			_make_graph(filename, dep_info, sect, '')
		
		ext_import_graph_filename = self.config.ext_import_graph
		if ext_import_graph_filename:
			filename = '{}.{}'.format(basename, ext_import_graph_filename)
			_make_graph(filename, self._external_dependencies_info(),
			            sect, 'external ')
			
		int_import_graph_filename = self.config.int_import_graph
		if int_import_graph_filename:
			filename = '{}.{}'.format(basename, int_import_graph_filename)
			_make_graph(filename, self._internal_dependencies_info(),
			            sect, 'internal ')
			
	ImportsChecker._report_dependencies_graph = new_report_dependencies_graph
		
		
		
		
def _override_make_graph():
	
	old_make_graph = _make_graph
	
	def new_make_graph(filename, dep_info, sect, gtype):
		pass
		
#config.load_results(self.file_state.base_name)
#self.reporter.on_close(self.stats, previous_stats)

def _get_pdata_path(base_name, recurs):
	base_name = base_name.replace(os.sep, '_')
	return os.path.join(PYLINT_HOME, "%s%s%s" % (base_name, recurs, '.stats'))
	
'''	def generate_reports(self):
		"""close the whole package /module, it's time to make reports !

		if persistent run, pickle results for later comparison
		"""
		# Display whatever messages are left on the reporter.
		self.reporter.display_messages(report_nodes.Section())

		if self.file_state.base_name is not None:
			previous_stats = config.load_results(self.file_state.base_name)
	
			self.reporter.on_close(self.stats, previous_stats)      ####################
			if self.config.reports:
				sect = self.make_reports(self.stats, previous_stats)
			else:
				sect = report_nodes.Section()

			if self.config.reports:
				self.reporter.display_reports(sect)
			self._report_evaluation()
			
			if self.config.persistent:
				config.save_results(self.stats, self.file_state.base_name)
		else:
			self.reporter.on_close(self.stats, {})
'''


if __name__ == '__main__': print(__file__)