from PyQt4 import QtCore,QtGui
from datetime import date
from .core import NumerologyReport

class BasicReportWidget(QtGui.QWidget):
	def __init__(self, report, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QFormLayout(self)
		layout.addRow("Life Path:", QtGui.QLabel(str(self.report.life_path_num)))
		layout.addRow("Birthday:", QtGui.QLabel(str(self.report.birth_day_num)))
		layout.addRow("Character:", QtGui.QLabel(str(self.report.character_num)))
		layout.addRow("Social:", QtGui.QLabel(str(self.report.social_num)))
		layout.addRow("Heart's Desire:", QtGui.QLabel(str(self.report.heart_num)))
		layout.addRow("First Vowel:", QtGui.QLabel(str(self.report.first_vowel_num)))
		layout.addRow("Rational Thought:", QtGui.QLabel(str(self.report.rational_thought_num)))
		layout.addRow("Balance:", QtGui.QLabel(str(self.report.balance_num)))
		layout.addRow("Underlying Goal:", QtGui.QLabel(str(self.report.underlying_goal_num)))
		layout.addRow("Capstone:", QtGui.QLabel(str(self.report.capstone_num)))
		layout.addRow("Cornerstone:", QtGui.QLabel(str(self.report.cornerstone_num)))

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
		for s in totals.keys():
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
		for s in totals2.keys():
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
		layout=QtGui.QFormLayout(self)
		self.dateedit=QtGui.QDateEdit(self)
		self.dateedit.setDisplayFormat("MM/dd/yyyy")
		self.dateedit.setCalendarPopup(True)
		self.dateedit.dateChanged.connect(self.updateDisplay)
		layout.addRow("Date:", self.dateedit)

		self.pdisplay=QtGui.QLabel()
		self.mdisplay=QtGui.QLabel()
		self.sdisplay=QtGui.QLabel()
		self.edisplay=QtGui.QLabel()
		layout.addRow("Physical:",self.pdisplay)
		layout.addRow("Mental:",self.mdisplay)
		layout.addRow("Spiritual:",self.sdisplay)
		layout.addRow("Essence:",self.edisplay)

		self.pydisplay=QtGui.QLabel()
		self.pmdisplay=QtGui.QLabel()
		self.pddisplay=QtGui.QLabel()
		layout.addRow("Personal Year:",self.pydisplay)
		layout.addRow("Personal Month:",self.pmdisplay)
		layout.addRow("Personal Day:",self.pddisplay)

		self.dateedit.setDate(date.today())
	def updateDisplay(self, date):
		date=date.toPyDate()
		p,m,s,e=self.report.transit_cycle_num(date)
		self.pdisplay.setText(str(p))
		self.mdisplay.setText(str(m))
		self.sdisplay.setText(str(s))
		self.edisplay.setText(str(e))

		pdatenums=self.report.personal_date_nums(date)
		self.pydisplay.setText(str(pdatenums["year"]))
		self.pmdisplay.setText(str(pdatenums["month"]))
		self.pddisplay.setText(str(pdatenums["day"]))

class NumerologyReportWidget(QtGui.QWidget):
	def __init__(self, report, l2nmapname, parent=None):
		super().__init__(parent)
		self.report=report
		layout=QtGui.QVBoxLayout(self)
		label=QtGui.QLabel(("Report for {}, born on {} and using"
							" the {} letter to number mapping.").format(self.report.full_name,
																		self.report.bdate,l2nmapname))
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
