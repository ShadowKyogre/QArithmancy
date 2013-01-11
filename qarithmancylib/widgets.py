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
		layout.addWidget(QtGui.QLabel("First Vowel:"),5,0)
		layout.addWidget(QtGui.QLabel(str(self.report.first_vowel_num)),5,1)
		layout.addWidget(QtGui.QLabel("Rational Thought:"),6,0)
		layout.addWidget(QtGui.QLabel(str(self.report.rational_thought_num)),6,1)
		layout.addWidget(QtGui.QLabel("Balance:"),7,0)
		layout.addWidget(QtGui.QLabel(str(self.report.balance_num)),7,1)
		layout.addWidget(QtGui.QLabel("Underlying Goal:"),8,0)
		layout.addWidget(QtGui.QLabel(str(self.report.underlying_goal_num)),8,1)
		layout.addWidget(QtGui.QLabel("Capstone:"),9,0)
		layout.addWidget(QtGui.QLabel(str(self.report.capstone_num)),9,1)
		layout.addWidget(QtGui.QLabel("Cornerstone:"),10,0)
		layout.addWidget(QtGui.QLabel(str(self.report.cornerstone_num)),10,1)

class StrengthandWeaknessWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QGridLayout(self)
		layout.addWidget(QtGui.QLabel("Hidden Passion:"),0,0)
		layout.addWidget(QtGui.QLabel(str(self.report.hidden_passion)),0,1)
		layout.addWidget(QtGui.QLabel("Subconscious Self:"),1,0)
		layout.addWidget(QtGui.QLabel(str(self.report.subconscious_self)),1,1)
		layout.addWidget(QtGui.QLabel("Possible weaknesses:"),2,0)
		hbox=QtGui.QHBoxLayout(self)
		layout.addLayout(hbox,2,1)
		for i in self.report.possible_weaknesses:
			hbox.addWidget(QtGui.QLabel(str(i)))

		layout.addWidget(QtGui.QLabel(("Planes of Expression:")),3,0,1,2)
		table=QtGui.QTableWidget(self)
		table.setRowCount(1)
		table.setColumnCount(4)
		table.setHorizontalHeaderLabels(("Physical","Emotional","Mental","Intuitive"))
		table.verticalHeader().hide()
		table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		area,area2,totals,totals2=self.report.planes_of_expression
		layout.addWidget(table,4,0,1,2)
		counter=0
		highlight=QtGui.QPalette().midlight().color()
		highlight.setAlpha(64)
		for s in ("physical","emotional","mental","intuitive"):
			item=QtGui.QTableWidgetItem()
			if s == area:
				item.setBackground(QtGui.QBrush(highlight))
			item.setText(str(totals[s]))
			table.setItem(0,counter,item)
			counter+=1
		else:
			counter=0
		table2=QtGui.QTableWidget(self)
		table2.setRowCount(1)
		table2.setColumnCount(3)
		table2.setHorizontalHeaderLabels(("Creative","Vacillating","Grounded"))
		table2.verticalHeader().hide()
		table2.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table2.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		for s in ("creative","vacillating","grounded"):
			item=QtGui.QTableWidgetItem()
			if s == area2:
				item.setBackground(QtGui.QBrush(highlight))
			item.setText(str(totals2[s]))
			table2.setItem(0,counter,item)
			counter+=1
		else:
			counter=0
		table.resizeRowsToContents()
		table2.resizeRowsToContents()
		layout.addWidget(table2,5,0,1,2)


class LifeViewWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QGridLayout(self)

		layout.addWidget(QtGui.QLabel("Challenges:"),0,0,1,2)
		counter=2
		for i in report.challenge_nums:
			layout.addWidget(QtGui.QLabel(str(i)),0,counter)
			counter+=1
		layout.addWidget(QtGui.QLabel("Pinnacles:"),1,0,1,3)
		layout.addWidget(QtGui.QLabel("Life Cycle:"),1,3,1,3)
		table=QtGui.QTableWidget(self)
		layout.addWidget(table,2,0,1,3)
		table.setColumnCount(4)
		table.setRowCount(2)
		table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table.setVerticalHeaderLabels(("End Age","Number"))
		pends,pnums=self.report.pinnacles
		for i in range(4):
			item=QtGui.QTableWidgetItem()
			item.setText(str(pends[i]))
			table.setItem(0,i,item)
		for i in range(4):
			item=QtGui.QTableWidgetItem()
			item.setText(str(pnums[i]))
			table.setItem(1,i,item)
		table2=QtGui.QTableWidget(self)
		layout.addWidget(table2,2,3,1,3)
		table2.setColumnCount(3)
		table2.setRowCount(2)
		table2.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table2.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		table2.setVerticalHeaderLabels(("End Age","Transition Age"))
		cycles=self.report.life_cycles
		for i in range(3):
			item=QtGui.QTableWidgetItem()
			item2=QtGui.QTableWidgetItem()
			item.setText(str(cycles[i][0]))
			item2.setText(str(cycles[i][1]))
			table2.setItem(0,i,item)
			table2.setItem(1,i,item2)

class LifeSnapshotWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report

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
		lifesnapshot=LifeSnapshotWidget(report,parent=self)

		tabs=QtGui.QTabWidget(self)
		tabs.addTab(basic_report,"Basics")
		tabs.addTab(strandweak, "Strengths and Weaknesses")
		tabs.addTab(lifeview, "Life Overview")
		tabs.addTab(lifesnapshot, "Life Snapshot")

		layout.addWidget(tabs)
