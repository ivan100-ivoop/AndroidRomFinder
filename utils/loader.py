import threading
from PyQt5.QtGui import *

links = []


class DevicesList (threading.Thread):
	def __init__(self, data):
		threading.Thread.__init__(self)
		self.data = data
	def run(self):
		for i in [1,2,3,4,5,6,7,8,9]:
			self.data.devices.addItems(self.data.mod.Brand_LIST(i))

class ModelList (threading.Thread):
	def __init__(self, data, name):
		threading.Thread.__init__(self)
		self.data = data
		self.name = name
	def run(self):
		self.data.models.addItems(self.data.mod.Brand_Model_List(self.name))

def DownloadLink(data, model):
		data_s = data.mod.get_Download_LINK(model)
		database = data_s[0]
		database_url = data_s[1]
		data.title.setText(database["filename"])
		data.size.setText(database["size"])
		for decode_data in database_url:
			links.append(decode_data['link'])
			data.simple_model.appendRow(QStandardItem(decode_data['name']))