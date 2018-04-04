#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename = guireporter
# author= KGerring
# date = 3/17/18
# from startups import *
""" """
from __future__ import absolute_import, unicode_literals # isort:skip
__all__ = []
import sys # isort:skip
import os # isort:skip
import regex # isort:skip
import re # isort:skip
import linecache
import pylint.utils
import pylint.config
import pylint.lint

from pylint.reporters import BaseReporter
#from pylint.reporters.json import JSONReporter
#from pylint.reporters.ureports.text_writer import TextWriter

from lintful.plugins.base import Reporter, ReporterMessage

import PyQt5
from PyQt5 import Qt, QtGui, QtWidgets
from PyQt5.Qt import QWindow, QGuiApplication, QIODevice, QObject, QTemporaryDir, QTemporaryFile
from qtpy.QtWidgets import (QCheckBox, QDialog, QFrame, QGridLayout, QGroupBox,
                            QHBoxLayout, QLabel, QLineEdit,
                            QPushButton, QMenu, QMessageBox, QRadioButton,
                            QSizePolicy, QSpacerItem, QTableView, QTabWidget,
                            QTextEdit, QVBoxLayout, QWidget, QWidgetItem, QTreeWidgetItem, QTreeWidgetItemIterator)

from PyQt5.QtWidgets import *


from qtpy.compat import getsavefilename, getopenfilenames
from qtpy.QtCore import Qt, Signal, Slot

from PyQt5.QtGui import (QTextBlockUserData, QTextBlock, QTextBlockGroup, QGuiApplication,
                         QAbstractTextDocumentLayout, QTextDocument)

#PyQt5.QtWidgets
#spyder.widgets.sourcecode.codeeditor.TestWidget
#editor,setup_editor,setup_context_menu,shortcuts,set_text_from_file

#set_language,linenumbers_margin,linenumbers_color,linenumberarea,is_json
#insert_text,in_comment_or_string,go_to_next_warning,go_to_next_cell,go_to_line

#blockuserdata_list
#ed.get_outlineexplorer_data()
#QTextBlockUserData
from spyder.utils import encoding, sourcecode
from spyder.widgets.sourcecode.base import TextEditBaseWidget
from spyder.widgets.editortools import PythonCFM
from spyder.widgets.sourcecode.codeeditor import CodeEditor, TestWidget, BlockUserData
from spyder.utils.introspection.manager import IntrospectionManager
from spyder.widgets.editor import (FileInfo, ThreadManager, AnalysisThread, EditorStack, EditorPluginExample)
#spyder.utils.codeanalysis.check(), find_tasks
#process_code_analysis



'spyder.widgets.sourcecode.codeeditor.TestWidget'


def convert_to_result(msg):
	module_object = msg.module
	if msg.obj:
		module_object += ".%s" % msg.obj
	message = "(%s) %s: %s" % (msg.C, module_object, msg.msg)
	line = msg.line
	return (message, line)


def check_with_pylint(fname):
	from pylint.lint import PyLinter
	linter = PyLinter()
	linter._do_load()
	collector = linter._reporters['collector']()
	linter.set_reporter(collector)
	check = linter._parallel_check([fname])
	results = []
	for msg in linter.reporter.messages:
		module_object = msg.module
		if msg.obj:
			module_object += ".%s" % msg.obj
		message = "[%s] %s %s" % (msg.symbol, module_object, msg.msg)
		results.append((message, msg.line))
		
	return results
	
	


def test_pylint(fname):
	from spyder.utils.qthelpers import qapplication
	app = qapplication(test_time=5)
	win = TestWidget(None)
	win.show()
	win.load(fname)
	win.resize(900, 700)
	results = check_with_pylint(fname)
	win.editor.process_code_analysis(results)
	sys.exit(app.exec_())



class FileInfo(QObject):
	"""File properties"""
	analysis_results_changed = Signal()
	todo_results_changed = Signal()
	save_breakpoints = Signal(str, str)
	text_changed_at = Signal(str, int)
	edit_goto = Signal(str, int, str)
	send_to_help = Signal(str, str, str, str, bool)
	
	def __init__(self, filename, encoding, editor, new, threadmanager,
	             introspection_plugin):
		QObject.__init__(self)
		self.threadmanager = threadmanager
		self.filename = filename
		self.newly_created = new
		self.default = False      # Default untitled file
		self.encoding = encoding
		self.editor = editor
		self.path = []
		
		self.classes = (filename, None, None)
		self.analysis_results = []
		self.todo_results = []
		self.lastmodified = QFileInfo(filename).lastModified()
		
		self.editor.textChanged.connect(self.text_changed)
		self.editor.breakpoints_changed.connect(self.breakpoints_changed)
		
		self.pyflakes_results = None
		self.pep8_results = None
		self.pylint_results = None
		
	
	def text_changed(self):
		"""Editor's text has changed"""
		self.default = False
		self.text_changed_at.emit(self.filename,
		                          self.editor.get_position('cursor'))
	
	def get_source_code(self):
		"""Return associated editor source code"""
		return to_text_string(self.editor.toPlainText())
	
	def get_filename(self):
		return to_text_string(self.filename)
	
	def run_code_analysis(self, pylint_results, run_pyflakes = None, run_pep8 = None):
		"""Run code analysis"""
		
		run_pyflakes = run_pyflakes and codeanalysis.is_pyflakes_installed()
		run_pep8 = run_pep8 and \
		           codeanalysis.get_checker_executable('pycodestyle') is not None
		self.pylint_results = []
		self.pyflakes_results = []
		self.pep8_results = []
		if self.editor.is_python():
			enc = self.encoding.replace('-guessed', '').replace('-bom', '')
			source_code, enc = encoding.encode(self.get_source_code(), enc)
			if run_pyflakes:
				self.pyflakes_results = None
			if run_pep8:
				self.pep8_results = None
				
			if run_pylint:
				self.pylint_result = None
				
			if run_pyflakes:
				self.threadmanager.add_thread(codeanalysis.check_with_pyflakes,
				                              self.pyflakes_analysis_finished,
				                              source_code, self)
			if run_pep8:
				self.threadmanager.add_thread(codeanalysis.check_with_pep8,
				                              self.pep8_analysis_finished,
				                              source_code, self)
				
			if run_pylint:
				self.threadmanager.add_thread(check_with_pylint, self.pylint_analysis_finished, source_code, self)
				
	
	def pyflakes_analysis_finished(self, results):
		"""Pyflakes code analysis thread has finished"""
		self.pyflakes_results = results
		if self.pep8_results is not None:
			pass
			#self.code_analysis_finished()
	
	def pep8_analysis_finished(self, results):
		"""Pep8 code analysis thread has finished"""
		self.pep8_results = results
		if self.pyflakes_results is not None:
			pass
			#self.code_analysis_finished()
	
	def pylint_analysis_finished(self, results):
		self.pylint_results = results
		self.code_analysis_finished()
	
	
	def code_analysis_finished(self):
		"""Code analysis thread has finished"""
		self.set_analysis_results(self.pylint_results)
		self.analysis_results_changed.emit()
	
	def set_analysis_results(self, results):
		"""Set analysis results and update warning markers in editor"""
		self.analysis_results = results
		self.editor.process_code_analysis(results)
	
	def cleanup_analysis_results(self):
		"""Clean-up analysis results"""
		self.analysis_results = []
		self.editor.cleanup_code_analysis()
	
	def run_todo_finder(self):
		"""Run TODO finder"""
		if self.editor.is_python():
			self.threadmanager.add_thread(codeanalysis.find_tasks,
			                              self.todo_finished,
			                              self.get_source_code(), self)
	
	def todo_finished(self, results):
		"""Code analysis thread has finished"""
		self.set_todo_results(results)
		self.todo_results_changed.emit()
	
	def set_todo_results(self, results):
		"""Set TODO results and update markers in editor"""
		self.todo_results = results
		self.editor.process_todo(results)
	
	def cleanup_todo_results(self):
		"""Clean-up TODO finder results"""
		self.todo_results = []
	
	def breakpoints_changed(self):
		"""Breakpoint list has changed"""
		breakpoints = self.editor.get_breakpoints()
		if self.editor.breakpoints != breakpoints:
			self.editor.breakpoints = breakpoints
			self.save_breakpoints.emit(self.filename, repr(breakpoints))







class LintFileInfo(FileInfo):pass


class Editor(object):
	blockuserdata_list = []
	


"""
Qt.QListWidget
Qt.QListWidgetItem

Qt.QTextDocument
Qt.QTextTable

Qt.QWindow
Qt.QPageLayout
Qt.QGuiApplication
Qt.QFileOpenEvent
Qt.QDir #QDir(path: str = '')

Qt.QFile
Qt.QFileInfo
Qt.QHistoryState

Qt.QFileDevice
Qt.QJsonDocument
Qt.QJsonValue
Qt.QRunnable
Qt.QSaveFile
Qt.QSharedMemory
Qt.QSignalMapper
Qt.QStandardPaths
Qt.QTemporaryDir
Qt.QTemporaryFile
Qt.QObject
Qt.QFrame

spyder.utils.qthelpers import action2button
"""


#QSharedMemory(str, parent: QObject = None)

#return getline(abspath, line)[column:].strip()


#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__

#msg_frame

def search_qt(text):
	from PyQt5 import Qt
	
	return [(d, getattr(qt, d)) for d in dir(Qt) if text in d.lower()]


BOXES = dict(check = QCheckBox,
             combo =QComboBox,
             group =QButtonGroup,
             radio =QRadioButton,
             push = QPushButton,
             command =QCommandLinkButton)


class PyLintGui(QMainWindow):
	
	def __init__(self):
		QMainWindow.__init__(self)
		#self.widget = QWidget(self)
		
		
		self.button_group = QButtonGroup()
		
		self.checkbox = QCheckBox()
		
		self.group0 = QGroupBox("Message Types Box")
		self.information_box = QCheckBox("Information")
		self.convention_box = QCheckBox('Convention')
		vbox = QVBoxLayout()
		vbox.addWidget(self.information_box)
		vbox.addWidget(self.convention_box)
		
		
		layout = QGridLayout(self)
		layout.addWidget(self.group0)
		self.setCentralWidget(layout)
	



def test():
	from PyQt5.QtWidgets import QApplication
	app = QGuiApplication([])
	_app = QApplication([])
	win = PyLintGui()
	win.show()
	



if __name__ == '__main__':
	test_pylint(__file__)