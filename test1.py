import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
host='127.0.0.1'
port=3306
def dbNameSearch():
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor = conn.cursor()
	createsql='show databases'
	cursor.execute(createsql)
	conn.commit()	
	data = cursor.fetchall()
	dataList=[item[0] for item in data]
	return(dataList)
def tableNameSearch(dbName):	
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql0="show tables;"
	cursor.execute(sql0)
	#conn.commit()
	data = cursor.fetchall()
	dataList1=[item[0] for item in data]
	return(dataList1)
def textpostion(i):
	return(50+i*30)
class dbTree(QMainWindow):
	def __init__(self, parent=None):
		super(dbTree, self).__init__(parent)
		self.setWindowTitle('TreeWidget 例子')
		self.dataList=dbNameSearch()
		self.resize(308, 900)
		self.tree=QTreeWidget(self)
		self.tree.setGeometry(QtCore.QRect(5, 10, 301, 371))
		self.pushButton = QtWidgets.QPushButton(self)
		self.pushButton.setGeometry(QtCore.QRect(110, 850, 75, 31))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setText("确定")
		self.pushButton.clicked.connect(self.btnpress)		
		self.tree.setColumnCount(1)
		self.tree.setHeaderLabels(['Key'])
		root=QTreeWidgetItem(self.tree)
		root.setText(0,'Mysql')
		self.tree.setColumnWidth(0,150)
		child1=QTreeWidgetItem()
		child1.setText(0,'child1')
		child1.setCheckState(0,Qt.Unchecked)
		root.addChild(child1)
		self.numList=[]
		self.dict={}
		for nameNum in range(len(self.dataList)):
			n = setattr(self, "cb%d" % nameNum, QTreeWidgetItem(root))
			m = getattr(self, "cb%d" % nameNum)
			m.setText(0,self.dataList[nameNum])
			root.addChild(m)
			tableNameList=tableNameSearch(self.dataList[nameNum])
			for tableNum in range(len(tableNameList)):				
				l=setattr(self, "cb%d" % int(nameNum*1000+tableNum), QTreeWidgetItem(m))
				k=getattr(self, "cb%d" % int(nameNum*1000+tableNum))
				self.numList.append(int(nameNum*1000+tableNum))
				self.dict[int(nameNum*1000+tableNum)]=self.dataList[nameNum]+'+'+tableNameList[tableNum]
				k.setText(0,tableNameList[tableNum])
				k.setCheckState(0,Qt.Unchecked)
		print(self.numList)
		self.tree.addTopLevelItem(root)
		self.tree.clicked.connect(self.onClicked)
		self.setCentralWidget(self.tree)
	def onClicked(self,qmodeLindex):
		item=self.tree.currentItem()
		print('Key=%s'%(item.text(0)))
	def btnpress(self):
		L_check = []
		for pipe in (self.numList):
			m = getattr(self, "cb%d" % pipe)
			print(m.checkState(0))
			if m.checkState(0)==2:
				L_check.append(self.dict[pipe])
		print(L_check)
if __name__ == '__main__':
	app = QApplication(sys.argv)
	tree = TreeWidgetDemo()
	tree.show()
	sys.exit(app.exec_())
