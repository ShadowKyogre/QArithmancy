from PyQt4 import QtCore,QtGui
import os

import arithstr
from qarithmancyconfig import QArithmancyConfig

class AliasEditorDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent=None, *args):
		super().__init__(parent, *args)
	
	def createEditor(self, parent, option, index):
		p=QtGui.QLineEdit(parent)
		p.setAutoFillBackground(True)
		return p

	def setEditorData(self, editor, index):
		value = index.model().data(index, QtCore.Qt.EditRole)
		if value is None:
			editor.setText("")
		else:
			editor.setText(value)

	def setModelData(self, editor, model, index):
		model.setData(index, editor.text().split(';'), QtCore.Qt.UserRole)
		model.setData(index, editor.text(), QtCore.Qt.EditRole)
		#needs edit twice for some reason?

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)

class DateEditorDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent=None, *args):
		super().__init__(parent, *args)

	def createEditor(self, parent, option, index):
		p=QtGui.QDateEdit(parent)
		p.setDisplayFormat("MM/dd/yyyy")
		p.setAutoFillBackground(True)
		return p

	def setEditorData(self, editor, index):
		value = index.model().data(index, QtCore.Qt.UserRole)
		if value is None:
			editor.setDate(QtCore.QDate())
		else:
			editor.setDate(value)

	def setModelData(self, editor, model, index):
		model.setData(index, editor.date(), QtCore.Qt.UserRole)
		model.setData(index, editor.date().toString("MM/dd/yyyy"), QtCore.Qt.EditRole)

	def updateEditorGeometry(self, editor, option, index):
		editor.setGeometry(option.rect)

class QArithmancy(QtGui.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QArithmancy")
		self.listy=QtGui.QTreeView(self)
		self.listy.setModel(qtrcfg.people)
		self.setCentralWidget(self.listy)
		self.listy.setSortingEnabled(True)

		dateeditor=DateEditorDelegate(self.listy)
		aliaseditor=AliasEditorDelegate(self.listy)
		self.listy.setItemDelegateForColumn(3,dateeditor)
		self.listy.setItemDelegateForColumn(4,aliaseditor)

		exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('application-exit'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.close)

		saveAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-save'), 'Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.setStatusTip('Save')
		saveAction.triggered.connect(self.saveData)

		newAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-new'), 'New Person', self)
		newAction.setShortcut('Ctrl+N')
		newAction.setStatusTip('New Person')
		newAction.triggered.connect(self.addPerson)

		deleteAction = QtGui.QAction(QtGui.QIcon.fromTheme('edit-delete'), 'Delete Person', self)
		deleteAction.setShortcut('Delete')
		deleteAction.setStatusTip('Delete Person')
		deleteAction.triggered.connect(self.deletePerson)

		viewAction = QtGui.QAction(QtGui.QIcon.fromTheme('document-open'), 'View Report for Person', self)
		viewAction.setShortcut('Ctrl+O')
		viewAction.setStatusTip('View Report for Person')
		viewAction.triggered.connect(self.viewPerson)

		toolbar = self.addToolBar('Exit')
		toolbar.addAction(exitAction)
		toolbar.addAction(saveAction)
		toolbar.addAction(newAction)
		toolbar.addAction(deleteAction)
		toolbar.addAction(viewAction)
		#toolbar.addAction(saveIMGAction)

	def closeEvent(self, event):
		qtrcfg.save_settings()
		super().closeEvent(event)

	def addPerson(self):
		item=QtGui.QStandardItem("Joe")
		item2=QtGui.QStandardItem("is")
		item3=QtGui.QStandardItem("Missing")
		item4=QtGui.QStandardItem("01/01/2000")
		item4.setData(QtCore.QDate(),QtCore.Qt.UserRole)
		item5=QtGui.QStandardItem("This is filler text")
		item5.setData(["This is filler text"],QtCore.Qt.UserRole)
		qtrcfg.people.appendRow([item,item2,item3,item4,item5])

	def deletePerson(self):
		item=self.listy.currentIndex()
		self.tree.model().takeRow(item.row())
	
	def viewPerson(self):
		item=self.listy.currentIndex()
		QtGui.QMessageBox.information(self,"a","a")

	def saveData(self,filename=None):
		if not filename:
			filename=QtGui.QFileDialog.getSaveFileName(self, caption="Save Current Reading",
				filter="Images (%s);;Text (*.txt)" %(' '.join(formats)))
		if filename:
			fmt=filename.split(".",1)[-1]
			if fmt == 'txt':
				self.saveDataAsTXT(filename)
			elif "*.{}".format(fmt) in formats:
				self.saveDataAsIMG(filename,fmt)
			else:
				QtGui.QMessageBox.critical(self, "Save Current Reading", \
				"Invalid format ({}) specified for {}!".format(fmt,filename))

def main():
	global formats
	global app
	global qtrcfg

	app = QtGui.QApplication(os.sys.argv)
	app.setApplicationName(QArithmancyConfig.APPNAME)
	app.setApplicationVersion(QArithmancyConfig.APPVERSION)
	qtrcfg = QArithmancyConfig()
	#app.setWindowIcon(QtGui.QIcon.fromTheme("qtarot"))
	window = QArithmancy()
	window.show()
	os.sys.exit(app.exec_())

if __name__ == "__main__":
	main()

