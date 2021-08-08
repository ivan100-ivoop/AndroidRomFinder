from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import threading
import webbrowser

from os import listdir
from os import path as pt
from os.path import isfile, join
import importlib
from utils import loader as md
from main_window_gui import Ui_MainWindow

mpath = "modules/"    
pt.join(mpath)
app = None

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mod = None
        self.setupUi(self)
        self.simple_model = QStandardItemModel()
        self.list_download.setModel(self.simple_model)
        self.modle_support.currentTextChanged.connect(self.startup)
        self.list_download.clicked.connect(self.onClicked)
        self.btn_find.clicked.connect(self.find)
        self.btn_visit.clicked.connect(self.visit)
        self.devices.currentTextChanged.connect(self.selected)
        self.response = None
        self.getModule()

    def visit(self):
        webbrowser.open(self.mod.DB_URL)

    def getModule(self):
        modules = [f.split('.py')[0] for f in listdir(mpath) if isfile(join(mpath, f))]
        self.modle_support.addItems(modules)
        
    def startup(self):
        self.devices.clear()
        self.models.clear()
        self.title.setText("")
        self.size.setText("")
        self.simple_model.clear()
        spath = mpath + self.modle_support.currentText() + ".py"
        print("Path: {}".format(spath))
        spec = importlib.util.spec_from_file_location("module." + self.modle_support.currentText(), spath)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        self.mod = foo
        self.DetectDevices()
        #print("Loading: {}".format(self.mod.DB_URL))
        
    def DetectDevices(self):
    	self.response = md.DevicesList(self)
    	self.response.start()

    def selected(self, value):
    	if self.response != None:
    		self.response = None
    	self.models.clear()
    	self.response = md.ModelList(self, value)
    	self.response.start()
    	self.response.join()
    	self.response = None

    def find(self):
    	model_name = self.models.currentText()
    	md.DownloadLink(self, model_name)

    def onClicked(self, index):
        item_id = index.row()
        link = md.links[item_id]
        webbrowser.open(link)
        app.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())