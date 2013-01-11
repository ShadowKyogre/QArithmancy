from PyQt4 import QtCore,QtGui

class AliasEditorDelegate(QtGui.QStyledItemDelegate):
	def __init__(self, parent=None, *args):
		super().__init__(parent, *args)
	
	def createEditor(self, parent, option, index):
		p=QtGui.QComboBox(parent)
		p.setAutoFillBackground(True)
		p.setEditable(True)
		return p

	def setEditorData(self, editor, index):
		value = index.model().data(index, QtCore.Qt.UserRole)
		print(index.row(), index.column())
		print(value)
		if value is not None:
			editor.addItems(value)

	def setModelData(self, editor, model, index):
		data = [editor.itemText(i) for i in range(editor.count())]
		model.setData(index, data, QtCore.Qt.UserRole)
		model.setData(index, ';'.join(data), QtCore.Qt.EditRole)
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
