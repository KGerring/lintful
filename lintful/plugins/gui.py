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

import guidata
#import guidata.qt
#import guidata.qtwidgets
#import guidata.dataset.qtwidgets
#import guidata.dataset.qtitemwidgets
from guidata import qt
import guidata.dataset.datatypes as datatypes
import guidata.dataset.dataitems as dataitems
from guidata.dataset import qtitemwidgets, qtwidgets

from guidata.dataset.datatypes import (ActivableDataSet, BeginGroup, BeginTabGroup, DataItem, DataItemProxy, DataItemVariable, DataSet, DataSetGroup, DataSetMeta, EndGroup, EndTabGroup, FormatProp, FuncProp, GetAttrProp, GroupItem, ItemProperty, Meta_Py3Compat, NoDefault, NotProp, Obj, ObjectItem, TabGroupItem, ValueProp,  update_dataset)


from guidata.dataset.qtitemwidgets import DataSetWidget

from guidata.dataset.qtwidgets import (DataSetShowLayout,
	DataSetEditDialog, DataSetEditGroupBox, DataSetEditLayout,
	DataSetGroupEditDialog, DataSetShowDialog, DataSetShowGroupBox,
	DataSetShowWidget)

from guidata.qt.QtGui import QMainWindow, QSplitter

from guidata.dataset.datatypes import (DataSet, BeginGroup, EndGroup,
                                       BeginTabGroup, EndTabGroup)

from guidata.dataset.dataitems import (BoolItem, ButtonItem, ChoiceItem,
                                       DataItem, DateItem, DateTimeItem, DictItem,
                                       DirectoryItem, FileOpenItem,
                                       FileSaveItem, FilesOpenItem, FirstChoice,
                                       FloatArrayItem, FloatItem, IntItem, ItemProperty, MultipleChoiceItem, NumericTypeItem,
                                       StringItem, TextItem
                                       )

from guidata.utils import restore_dataset, bind, update_dataset

#guidata.tests.editgroupbox.ExampleMultiGroupDataSet
# guidata.guitest.TestLauncherWindow(guidata)
# win.show()

all_by_module = {
	
	'guidata.dataset.datatypes':
		['ActivableDataSet', 'BeginGroup', 'BeginTabGroup', 'DataItem', 'DataItemProxy', 'DataItemVariable', 'DataSet', 'DataSetGroup', 'DataSetMeta', 'EndGroup', 'EndTabGroup', 'FormatProp', 'FuncProp', 'GetAttrProp', 'GroupItem', 'ItemProperty', 'Meta_Py3Compat', 'NoDefault', 'NotProp', 'Obj', 'ObjectItem', 'TabGroupItem', 'ValueProp', 'to_text_string', 'update_dataset'],
	
	'guidata.utils': ['add_extension'],
	
	'guidata.dataset.dataitems': ['BoolItem', 'ButtonItem', 'ChoiceItem', 'ColorItem', 'DataItem', 'DateItem', 'DateTimeItem', 'DictItem', 'DirectoryItem', 'FileOpenItem', 'FileSaveItem', 'FilesOpenItem', 'FirstChoice', 'FloatArrayItem', 'FloatItem', 'FontFamilyItem', 'ImageChoiceItem', 'IntItem', 'ItemProperty', 'MultipleChoiceItem', 'NumericTypeItem', 'StringItem', 'TextItem']
}
from guidata.qt.QtGui import QMainWindow
from guidata.qthelpers import create_action, add_actions, get_std_icon

#qapplication
from guidata.tests.editgroupbox import MainWindow as Window, OtherDataSet
from guidata.tests.callbacks import TestParameters
#register_reporter(CollectingReporter)



#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


class PyLintSelectDataSet(DataSet):
	
	def cb_run_button(self, item, value, parent=None):
		print("\nitem: ", item, "\nvalue:", value)
		if self.results is None:
			self.results = ''
		self.results += str(value) + '\n'
		print("results:", self.results)
		#return value
	
	def cb_run_files(self, item, value):
		print("\nitem: ", item, "\nvalue:", value)
		#self.dictitem.set_default('files', [])
		if self.openfiles is not None:
			self.dictitem['files'].extend(self.openfiles)
		else:
			self.dictitem['files'].extend([])
		#
		#if self.dictitem is None:
		#	self.dictitem = {}
		#for i,v in enumerate(value):
		#	self.dictitem[i]  = v
		print(self.dictitem)
	
	openfiles = FilesOpenItem('lint files', formats='py',
	                          check=True).set_prop('display', callback=cb_run_files)
	opendirectory = DirectoryItem('lint_directory',
		default='/Users/kristen/PycharmProjects/proj/lintful/lintful')
	
	run_button = ButtonItem('run_linter', callback =cb_run_button, default = False)
	#run_button.bind(ResponsiveDataSet)
	#ditem = DataItem('data', True)
	results = TextItem("Results")
	dictitem = DictItem('dictionary', default = {'files': []}).set_prop("display", active=True)


class ResponsiveDataSet(DataSet):
	#DataSetEditGroupBox
	#SIG_APPLY_BUTTON_CLICKED.connect(self.update_window)
	#self.update_groupboxes()
	
	def cb_example(self, item, value):
		print("\nitem: ", item, "\nvalue:", value)
		if self.results is None:
			self.results = ''
		self.results += str(value) + '\n'
		print("results:", self.results)
	
	string = StringItem("String", default="foobar"
	                    ).set_prop("display", callback=cb_example)
	results = TextItem("Results")
	
		
class MWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setWindowTitle("Application example")
		self.groupbox = DataSetEditGroupBox("Standard dataset", OtherDataSet, comment='')
		#self.dialog = guidata.dataset.qtwidgets.DataSetEditDialog(self.groupbox)
		splitter = QSplitter(self)
		splitter.addWidget(self.groupbox)
		
		
#connectNotify,clicked,SIG_APPLY_BUTTON_CLICKED

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setWindowTitle("Application example")
		file_menu = self.menuBar().addMenu("File")
		quit_action = create_action(self, "Quit",
		                            shortcut="Ctrl+Q",
		                            icon=get_std_icon("DialogCloseButton"),
		                            tip="Quit application",
		                            triggered=self.close)
		add_actions(file_menu, (quit_action,))
		edit_menu = self.menuBar().addMenu("Edit")
		
		self.groupbox = DataSetEditGroupBox("Standard dataset", OtherDataSet, comment='')
		self.groupbox.SIG_APPLY_BUTTON_CLICKED.connect(self.update_window)
		self.display = DataSetEditGroupBox("Read-only dataset", OtherDataSet, comment='')
		
		splitter = QSplitter(self)
		splitter.addWidget(self.groupbox)
		self.setCentralWidget(splitter)
		self.setContentsMargins(10, 5, 10, 5)
		
	def update_window(self):
		dataset = self.groupbox.dataset
		self.setWindowTitle(dataset.title)
		self.setWindowIcon(get_icon(dataset.icon))
		self.setWindowOpacity(dataset.opacity)
		update_dataset(self.display, self.groupbox)
			
		
	def show_groupbox(self):
		show = DataSetShowGroupBox("Standard dataset", self.groupbox.dataset)
		return show
		
		
		
	def get_main(self):
		"""
		
		:return:
		"""
	MAINARGS = """
	
	from guidata.qt.QtGui import QApplication
	import sys
	import guidata
	_app = guidata.qapplication()
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	"""


def convert_to_string(msg):
	"""make a string representation of a message"""
	module_object = msg.module
	if msg.obj:
		module_object += ".%s" % msg.obj
	return "(%s) %s [%d]: %s" % (msg.C, module_object, msg.line, msg.msg)


class GuiStream(object):
	def __init__(self, gui):
		"""init"""
		self.curline = ""
		self.gui = gui
		self.contents = []
		self.outdict = {}
		self.currout = None
		self.next_title = None
	
	def write(self, text):
		"""write text to the stream"""
		if re.match('^--+$', text.strip()) or re.match('^==+$', text.strip()):
			if self.currout:
				self.outdict[self.currout].remove(self.next_title)
				self.outdict[self.currout].pop()
			self.currout = self.next_title
			self.outdict[self.currout] = ['']
		
		if text.strip():
			self.next_title = text.strip()
		
		if text.startswith(os.linesep):
			self.contents.append('')
			if self.currout:
				self.outdict[self.currout].append('')
		self.contents[-1] += text.strip(os.linesep)
		if self.currout:
			self.outdict[self.currout][-1] += text.strip(os.linesep)
		if text.endswith(os.linesep) and text.strip():
			self.contents.append('')
			if self.currout:
				self.outdict[self.currout].append('')
	
	def fix_contents(self):
		"""finalize what the contents of the dict should look like before output"""
		for item in self.outdict:
			num_empty = self.outdict[item].count('')
			for _ in range(num_empty):
				self.outdict[item].remove('')
			if self.outdict[item]:
				self.outdict[item].pop(0)
	
	def output_contents(self):
		"""output contents of dict to the gui, and set the rating"""
		self.fix_contents()
		self.gui.tabs = self.outdict
		try:
			self.gui.rating.set(self.outdict['Global evaluation'][0])
		except KeyError:
			self.gui.rating.set('Error')
		self.gui.refresh_results_window()
		
		#reset stream variables for next run
		self.contents = []
		self.outdict = {}
		self.currout = None
		self.next_title = None


class PyLintGui(QMainWindow):
	""""""
	
	def __init__(self, root=None):
		self.root = root
		self.reporter = None
		self.msg_queue = None
		self.msgs = []
		self.visible_msgs = []
		self.filenames = []
		self.rating = ''
		self.rating_label = QLabel('Rating:', None)
		self.tabs = {}
		self.report_stream = GuiStream(self)
		self.lb_messages = None
		self.showhistory = None
		self.results = None
		self.btnRun = None
		
		self.information_box = None
		self.convention_box = None
		self.refactor_box = None
		self.warning_box = None
		self.error_box = None
		self.fatal_box = None
		
		self.txtModule = None
		self.status = None
		self.msg_type_dict = None
		
		
		
	def refresh_msg_window(self):
		self.lb_messages.delete(0, END)
		self.visible_msgs = []
		for msg in self.msgs:
			if self.msg_type_dict.get(msg.C)():
				self.visible_msgs.append(msg)
				msg_str = convert_to_string(msg)
				self.lb_messages.insert(END, msg_str)
				fg_color = COLORS.get(msg_str[:3], 'black')
				self.lb_messages.itemconfigure(END, fg=fg_color)
	
	def set_msg_type_dict(self):
		self.msg_type_dict = {
			'I': lambda: self.information_box.get() == 1,
			'C': lambda: self.convention_box.get() == 1,
			'R': lambda: self.refactor_box.get() == 1,
			'E': lambda: self.error_box.get() == 1,
			'W': lambda: self.warning_box.get() == 1,
			'F': lambda: self.fatal_box.get() == 1
		}

	def setup_msg_buttons(self):
		msg_buttons = qt.QtGui.QButtonGroup()
		
		self.information_button = qt.QtGui.QRadioButton('information')
		
		self.information_box = qt.QtGui.QCheckBox('information')
		
#QTextList
#QSessionManager
#QRadioButton
#QListWidgetItem
#QListView
#QListWidget
#QGroupBox
#QButtonGroup


if __name__ == '__main__':
	from guidata.qt.QtGui import QApplication
	app = QApplication(sys.argv)
	window = Window()
	window.show()