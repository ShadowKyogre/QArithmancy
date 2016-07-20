from PyQt4 import QtGui,QtCore
import csv
import os
from collections import OrderedDict as od

from .core import LetterMapping
from . import APPNAME, AUTHOR, MAPPINGS

class QArithmancyConfig:
    def __init__(self):
        self.settings=QtCore.QSettings(QtCore.QSettings.IniFormat,
                        QtCore.QSettings.UserScope,
                        AUTHOR,APPNAME)

        self.userconfdir=QtGui.QDesktopServices.storageLocation\
        (QtGui.QDesktopServices.DataLocation).replace("//","/")
        user_mappings=os.path.join(self.userconfdir,"mappings")

        self.sys_icotheme=QtGui.QIcon.themeName()
        self.reset_settings()
        QtCore.QDir.setSearchPaths("mappings", [user_mappings, MAPPINGS])
        self.load_people()
        self.load_mappings()
    
    def reset_settings(self):
        self.current_icon_override=self.settings.value("stIconTheme", "")
        if self.current_icon_override > "":
            QtGui.QIcon.setThemeName(self.current_icon_override)
        else:
            QtGui.QIcon.setThemeName(self.sys_icotheme)

    def changed_update(self, item):
        self.save_people()

    def add_delete_update(self, index, start, end):
        self.save_people()
    
    def load_mappings(self):
        self.mappings=od()
        mappings_path=QtCore.QDir("mappings:/")
        for i in mappings_path.entryList():
            if i in (".",".."):
                continue
            mapping=mappings_path.absoluteFilePath(i)
            self.mappings[os.path.splitext(i)[0].title()]=LetterMapping(mapping)

    def load_people(self):
        self.people=QtGui.QStandardItemModel()
        self.people.setColumnCount(4)
        self.people.setHorizontalHeaderLabels(["First Name","Middle Name",
                                        "Last Name","Birthdate"])
        path=os.path.join(self.userconfdir, 'people.csv')

        if not os.path.exists(path):
            if not os.path.exists(path.replace("people.csv","")):
                print("Making directory to store people")
                os.makedirs(self.userconfdir)
            from shutil import copyfile
            sch=os.path.join(os.sys.path[0],"people.csv")
            copyfile(sch, path)
        planner = csv.reader(open(path, "r"))
        next(planner)

        for entry in planner:
            if len(entry) == 0:
                continue
            first_column=QtGui.QStandardItem()
            second_column=QtGui.QStandardItem()
            third_column=QtGui.QStandardItem()
            fourth_column=QtGui.QStandardItem()
            #fifth_column=QtGui.QStandardItem()

            first_column.setText(entry[0])
            second_column.setText(entry[1])
            third_column.setText(entry[2])
            fourth_column.setText(entry[3])
            #nicks = tuple(entry[4].split(";"))
            #print(nicks)
            #if len(nicks) == 0:
            #   fifth_column.setText("<No nicknames>")
            #elif len(nicks) == 1:
            #   fifth_column.setText(nicks[0])
            #else:
            #   fifth_column.setText("{} and {} other nicknames".format(nicks[0],len(nicks[1:])))
            #fifth_column.setData(nicks)
            #print(fifth_column.data(QtCore.Qt.UserRole))
            if QtCore.QDate.fromString(entry[3], "MM/dd/yyyy").isValid():
                fourth_column.setData(QtCore.QDate.fromString(entry[3], "MM/dd/yyyy"),QtCore.Qt.UserRole)
            else:
                fourth_column.setData(QtCore.QDate(),QtCore.Qt.UserRole)

            self.people.appendRow([first_column,second_column,third_column,fourth_column])
        self.people.rowsInserted.connect(self.add_delete_update)
        self.people.rowsRemoved.connect(self.add_delete_update)
        self.people.itemChanged.connect(self.changed_update)

    def save_people(self):
        rows=self.people.rowCount()
        path=os.path.join(self.userconfdir, 'people.csv')
        temppath=os.path.join(self.userconfdir, 'people_modified.csv')
        f=open(temppath, "w")
        planner = csv.writer(f)
        planner.writerow(["First Name","Middle Name",
                        "Last Name","Birthdate"])
        for i in range(rows):
            first_column=self.people.item(i,0).text()
            second_column=self.people.item(i,1).text()
            third_column=self.people.item(i,2).text()
            fourth_column=self.people.item(i,3).data(QtCore.Qt.UserRole).toString("MM/dd/yyyy")  #need format like this: %m/%d/%Y
            #fifth_column=self.people.item(i,4).text()
            planner.writerow([first_column,second_column,third_column,fourth_column])
        f.close()
        os.remove(path)
        os.renames(temppath, path)

    def save_settings(self):
        self.settings.setValue("stIconTheme",self.current_icon_override)
        self.settings.sync()    


