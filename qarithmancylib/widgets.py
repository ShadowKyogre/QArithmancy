from PyQt4 import QtCore,QtGui
from .core import NumerologyReport

class BasicReportWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QGridLayout(self)
		layout.addWidget(QtGui.QLabel("Life Path:"),0,0)
		layout.addWidget(QtGui.QLabel(str(self.report.life_path_num)),0,1)
		layout.addWidget(QtGui.QLabel("Birthday:"),1,0)
		layout.addWidget(QtGui.QLabel(str(self.report.birth_day_num)),1,1)
		layout.addWidget(QtGui.QLabel("Character:"),2,0)
		layout.addWidget(QtGui.QLabel(str(self.report.character_num)),2,1)
		layout.addWidget(QtGui.QLabel("Social:"),3,0)
		layout.addWidget(QtGui.QLabel(str(self.report.social_num)),3,1)
		layout.addWidget(QtGui.QLabel("Heart's Desire:"),4,0)
		layout.addWidget(QtGui.QLabel(str(self.report.heart_num)),4,1)


class StrengthandWeaknessWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QGridLayout(self)


class LifeViewWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QGridLayout(self)

class NumerologyReportWidget(QtGui.QWidget):
	def __init__(self, report, l2nmapname, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QVBoxLayout(self)
		label=QtGui.QLabel("Report for {}, born on {} and using the {} letter to number mapping."\
							.format(self.report.full_name,self.report.bdate,l2nmapname))
		layout.addWidget(label)
		
		basic_report=BasicReportWidget(report,parent=self)
		strandweak=StrengthandWeaknessWidget(report,parent=self)
		lifeview=LifeViewWidget(report,parent=self)

		tabs=QtGui.QTabWidget(self)
		tabs.addTab(basic_report,"Basics")
		tabs.addTab(strandweak, "Strengths and Weaknesses")
		tabs.addTab(lifeview, "Life Overview")

		layout.addWidget(tabs)
