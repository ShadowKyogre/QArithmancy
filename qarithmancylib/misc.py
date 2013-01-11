from PyQt4 import QtCore,QtGui

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
