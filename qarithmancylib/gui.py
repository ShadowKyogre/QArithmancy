from PyQt4 import QtCore,QtGui
import os
from datetime import date

from .core import NumerologyReport
from .widgets import NumerologyReportWidget
from .misc import AliasEditorDelegate, DateEditorDelegate
from .guiconfig import QArithmancyConfig
from . import APPNAME,APPVERSION,AUTHOR,DESCRIPTION,YEAR,PAGE,EMAIL

class QArithmancy(QtGui.QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("QArithmancy")
		self.listy=QtGui.QTreeView(self)
		self.listy.setModel(qtrcfg.people)
		self.setCentralWidget(self.listy)
		self.listy.setSortingEnabled(True)

		dateeditor=DateEditorDelegate(self.listy)
		#aliaseditor=AliasEditorDelegate(self.listy)
		self.listy.setItemDelegateForColumn(3,dateeditor)
		#self.listy.setItemDelegateForColumn(4,aliaseditor)

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

		aboutAction=QtGui.QAction(QtGui.QIcon.fromTheme('help-about'), 'About', self)
		aboutAction.triggered.connect(self.about)

		toolbar = self.addToolBar('Exit')
		toolbar.addAction(exitAction)
		toolbar.addAction(saveAction)
		toolbar.addAction(newAction)
		toolbar.addAction(deleteAction)
		toolbar.addAction(aboutAction)
		#http://www.ffuts.org/blog/right-aligning-a-button-in-a-qtoolbar/
		spacer = QtGui.QWidget()
		spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		toolbar.addWidget(spacer)
		self.mappingBox = QtGui.QComboBox()
		self.mappingBox.addItems(list(qtrcfg.mappings.keys()))
		toolbar.addWidget(QtGui.QLabel("Letter to number mapping"))
		toolbar.addWidget(self.mappingBox)
		toolbar.addAction(viewAction)

	def about(self):
		QtGui.QMessageBox.about (self, "About {}".format(APPNAME),
		("<center><big><b>{0} {1}</b></big>"
		"<br />{2}<br />(C) <a href=\"mailto:{3}\">{4}</a> {5}<br />"
		"<a href=\"{6}\">{0} Homepage</a></center>")\
		.format(APPNAME,APPVERSION,DESCRIPTION,EMAIL,AUTHOR,YEAR,PAGE))

	def closeEvent(self, event):
		qtrcfg.save_settings()
		super().closeEvent(event)

	def addPerson(self):
		item=QtGui.QStandardItem("Joe")
		item2=QtGui.QStandardItem("is")
		item3=QtGui.QStandardItem("Missing")
		item4=QtGui.QStandardItem("01/01/2000")
		item4.setData(QtCore.QDate(),QtCore.Qt.UserRole)
		#item5=QtGui.QStandardItem("This is filler text")
		#item5.setData(["This is filler text"],QtCore.Qt.UserRole)
		qtrcfg.people.appendRow([item,item2,item3,item4])

	def deletePerson(self):
		item=self.listy.currentIndex()
		self.listy.model().takeRow(item.row())
	
	def viewPerson(self):
		item=self.listy.currentIndex()
		mapping=qtrcfg.mappings[self.mappingBox.currentText()]
		dialog=QtGui.QDialog(self)
		layout=QtGui.QVBoxLayout(dialog)

		fname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 0), QtCore.Qt.EditRole)
		mname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 1), QtCore.Qt.EditRole)
		lname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 2), QtCore.Qt.EditRole)
		bdate=qtrcfg.people.data(qtrcfg.people.index(item.row(), 3), QtCore.Qt.UserRole)
		report=NumerologyReport(fname, lname, bdate.toPyDate(),
								mapping, middle_name=mname)
		reportw=NumerologyReportWidget(report, self.mappingBox.currentText(), parent=dialog)
		layout.addWidget(reportw)
		buttonbox=QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
		closebutton=buttonbox.addButton(QtGui.QDialogButtonBox.Close)
		closebutton.clicked.connect(dialog.close)
		layout.addWidget(buttonbox)
		dialog.show()

	def saveDataAsTXT(self,filename,sdate,edate):
		item=self.listy.currentIndex()
		mapping=qtrcfg.mappings[self.mappingBox.currentText()]
		fname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 0), QtCore.Qt.EditRole)
		mname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 1), QtCore.Qt.EditRole)
		lname=qtrcfg.people.data(qtrcfg.people.index(item.row(), 2), QtCore.Qt.EditRole)
		bdate=qtrcfg.people.data(qtrcfg.people.index(item.row(), 3), QtCore.Qt.UserRole)
		report=NumerologyReport(fname, lname, bdate.toPyDate(),
								mapping, middle_name=mname)
		report.export(filename,sdate,edate,self.mappingBox.currentText())

	def saveData(self,filename=None,sdate=None,edate=None):
		if None in (sdate,edate):
			dialog=QtGui.QDialog(self)
			layout=QtGui.QVBoxLayout(dialog)
			form=QtGui.QFormLayout()
			layout.addLayout(form)
			sdateinput=QtGui.QDateEdit()
			edateinput=QtGui.QDateEdit()
			sdateinput.setDisplayFormat("MM/dd/yyyy")
			edateinput.setDisplayFormat("MM/dd/yyyy")
			sdateinput.setDate(date.today())
			edateinput.setDate(date.today())
			buttonbox=QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
			okbutton=buttonbox.addButton(QtGui.QDialogButtonBox.Ok)
			form.addRow("Forecast start:",sdateinput)
			form.addRow("Forecast end:",edateinput)
			okbutton.clicked.connect(dialog.accept)
			cancelbutton=buttonbox.addButton(QtGui.QDialogButtonBox.Cancel)
			cancelbutton.clicked.connect(dialog.reject)
			layout.addWidget(buttonbox)
			retcode = dialog.exec()
			if retcode == QtGui.QDialog.Rejected:
				return
			else:
				edate=edateinput.date().toPyDate()
				sdate=sdateinput.date().toPyDate()
		if not filename:
			filename=QtGui.QFileDialog.getSaveFileName(self, caption="Save Current Report",
				filter="Text (*.txt)")
				#filter="Images (%s);;Text (*.txt)" %(' '.join(formats)))
		if filename:
			fmt=filename.split(".",1)[-1]
			if fmt == 'txt':
				self.saveDataAsTXT(filename,sdate,edate)
			#elif "*.{}".format(fmt) in formats:
			#	self.saveDataAsIMG(filename,fmt)
			else:
				QtGui.QMessageBox.critical(self, "Save Current Report", \
				"Invalid format ({}) specified for {}!".format(fmt,filename))

def main():
	#global formats
	global app
	global qtrcfg

	app = QtGui.QApplication(os.sys.argv)
	app.setApplicationName(APPNAME)
	app.setApplicationVersion(APPVERSION)
	qtrcfg = QArithmancyConfig()
	app.setWindowIcon(QtGui.QIcon.fromTheme(APPNAME.lower()))
	window = QArithmancy()
	window.show()
	os.sys.exit(app.exec_())

if __name__ == "__main__":
	main()

