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
import guidata.dataset.datatypes
import guidata.dataset.dataitems

from guidata.dataset.datatypes import (ActivableDataSet, BeginGroup, BeginTabGroup, DataItem, DataItemProxy, DataItemVariable, DataSet, DataSetGroup, DataSetMeta, EndGroup, EndTabGroup, FormatProp, FuncProp, GetAttrProp, GroupItem, ItemProperty, Meta_Py3Compat, NoDefault, NotProp, Obj, ObjectItem, TabGroupItem, ValueProp,  update_dataset)

from  guidata.dataset.dataitems import ItemProperty, TextItem, FilesOpenItem
from guidata.dataset.qtwidgets import DataSetEditLayout, DataSetShowLayout

from guidata.dataset.qtitemwidgets import DataSetWidget

from guidata.dataset.qtwidgets import (
	DataSetEditDialog, DataSetEditGroupBox, DataSetEditLayout,
	DataSetGroupEditDialog, DataSetShowDialog, DataSetShowGroupBox,
	DataSetShowWidget)

from guidata.qt.QtGui import QMainWindow, QSplitter

from guidata.dataset.datatypes import (DataSet, BeginGroup, EndGroup,
                                       BeginTabGroup, EndTabGroup)

#guidata.tests.editgroupbox.ExampleMultiGroupDataSet
# guidata.guitest.TestLauncherWindow(guidata)
# win.show()

all_by_module = {
	
	'guidata.dataset.datatypes':
		['ActivableDataSet', 'BeginGroup', 'BeginTabGroup', 'DataItem', 'DataItemProxy', 'DataItemVariable', 'DataSet', 'DataSetGroup', 'DataSetMeta', 'EndGroup', 'EndTabGroup', 'FormatProp', 'FuncProp', 'GetAttrProp', 'GroupItem', 'ItemProperty', 'Meta_Py3Compat', 'NoDefault', 'NotProp', 'Obj', 'ObjectItem', 'TabGroupItem', 'ValueProp', 'to_text_string', 'update_dataset'],
	
	'guidata.utils': ['add_extension'],
	
	'guidata.dataset.dataitems': ['BoolItem', 'ButtonItem', 'ChoiceItem', 'ColorItem', 'DataItem', 'DateItem', 'DateTimeItem', 'DictItem', 'DirectoryItem', 'FileOpenItem', 'FileSaveItem', 'FilesOpenItem', 'FirstChoice', 'FloatArrayItem', 'FloatItem', 'FontFamilyItem', 'ImageChoiceItem', 'IntItem', 'ItemProperty', 'MultipleChoiceItem', 'NumericTypeItem', 'StringItem', 'TextItem']
}

#qapplication
######from guidata.tests.editgroupbox import MainWindow as Window
######from guidata.tests.callbacks import TestParameters
#register_reporter(CollectingReporter)



#from startups.helpers.decorators import ExportsList
#__all__ = ExportsList(initlist = __all__, __file__ = __file__) # all-decorator: __all__


class PyLintGUIDataSet(DataSet):
	pass

class ResponsiveDataSet(DataSet):
	#DataSetEditGroupBox
	#SIG_APPLY_BUTTON_CLICKED.connect(self.update_window)
	#self.update_groupboxes()
	
	pass


from guidata.qt.QtGui import QMainWindow
from guidata.qthelpers import create_action, add_actions, get_std_icon

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
		
	def get_main(self):
		"""
		
		:return:
		"""
	MAINARGS = """
	from guidata.qt.QtGui import QApplication
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	"""



if __name__ == '__main__':
	from guidata.qt.QtGui import QApplication
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()