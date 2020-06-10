import sys
import base64
import sys, traceback
from waiting import img as waiting
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import (QFile, QFileInfo, QSettings,QTimer, Qt, QByteArray)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog,
		QMainWindow, QMessageBox, QShortcut, QTabWidget,
		QPlainTextEdit)
from PyQt5.QtGui import QIcon,QKeySequence
import resources_rc
import textedit
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pymysql
import re
import os
import shutil
from dialog import dialog_xml
from Shortcut import CJKshortcut
from Shortcut import shortcut
from Shortcut import CJKAdd
from Shortcut import shortcutAdd
from StringDefinition import IDS
from StringDefinition import biaodian
from help import hhc_shengcheng
from help import hhk_shengcheng
from help import help_xingui_tihuan
from mysqlAndexcel import excelToMysql,store_xls
from Extract import collect_all
from Extract import PS_PPD
from Extract import PS_RC
from Extract import Integrate


tmp = open('waiting.gif', 'wb+')
tmp.write(base64.b64decode(waiting))
tmp.close()
languageList=['JPN','ENU','CHS','CHT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
db='702_hhc'
table='hhc'
host='127.0.0.1'
port=3306
userdb='root'
passwdb='123456'
__version__ = "1.0.0"
fileName1=['hhc','hhk','stringdefinition','dialog_xml','dialog_xml_font','htm']
class checkboxListType(QWidget):

	def __init__(self,dbName,dir_choose):
		super().__init__()
		self.initUI()
		self.dbName=dbName
		self.dir_choose=dir_choose

	def initUI(self):
		# 新建4个复选框对象

		
		# lpostion=['50','80','110','140','170','200','230','260','290','320','350','380','410','440','470','500','530','560','590','620','650','680','710','740','770']
		l = fileName1
		sum = 0
		for nameNum in range(len(fileName1)):
			n = setattr(self, "cb%d" % nameNum, QCheckBox('%s' % (fileName1[nameNum]), self))
			m = getattr(self, "cb%d" % nameNum)
			m.move(30, textpostion(nameNum))
			sum = max(sum, textpostion(nameNum))
		# button.setFixedSize(QtCore.QSize(60,30))
		self.qxbtn = QCheckBox('all', self)
		# m=getattr(self,"cb%d"%pipe)


		bt = QPushButton('提交', self)

		self.resize(300, sum + 100)
		self.setWindowTitle('选择要复制的文件夹')

		self.qxbtn.move(20, 20)
		# self.cb2.move(30,50)
		# self.cb3.move(30,80)
		# self.cb4.move(30,110)

		bt.move(20, sum + 50)

		self.qxbtn.stateChanged.connect(self.changecb1)
		# self.cb2.stateChanged.connect(self.changecb2)
		# self.cb3.stateChanged.connect(self.changecb2)
		# self.cb4.stateChanged.connect(self.changecb2)
		bt.clicked.connect(self.go)
		bt.clicked.connect(self.close)

		self.show()

	def go(self):
		L_check = []
		for pipe in range(len(fileName1)):
			m = getattr(self, "cb%d" % pipe)
			if m.isChecked():
				# print("pipe"),
				L_check.append(fileName1[pipe])
			# print(pipe),
			# print("is selected!!!")
		print(123)
		print(L_check)
		self.L_check=L_check
		try:
			dialog=LoadingWindowPCL(host,port,self.dbName,self.dir_choose,self.L_check)
			dialog.exec_()

			QApplication.processEvents()
			QMessageBox.information(self, "提示",'抽取完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)
	def changecb1(self):
		if self.qxbtn.checkState() == Qt.Checked:
			for nameNum in range(len(fileName1)):
				m = getattr(self, "cb%d" % nameNum)
				m.setChecked(True)
		elif self.qxbtn.checkState() == Qt.Unchecked:
			for nameNum in range(len(fileName1)):
				m = getattr(self, "cb%d" % nameNum)
				m.setChecked(False)

	def changecb2(self):
		if self.cb2.isChecked() and self.cb3.isChecked() and self.cb4.isChecked():
			self.cb1.setCheckState(Qt.Checked)
		elif self.cb2.isChecked() or self.cb3.isChecked() or self.cb4.isChecked():
			self.cb1.setTristate()
			self.cb1.setCheckState(Qt.PartiallyChecked)
		else:
			self.cb1.setTristate(False)
			self.cb1.setCheckState(Qt.Unchecked)
			
class LoadingWindowIntegrateUnion(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,host,port,dbNameList,dbName):
		super(LoadingWindowIntegrateUnion, self).__init__()
		self.host=host
		self.port=port
		self.dbNameList=dbNameList
		self.dbName=dbName
		self.thread = WorkerIntegrateUnion(host,port,dbNameList,dbName)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowPCL):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerIntegrateUnion(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,host,port,dbNameList,dbName,parent=None):
		super(WorkerIntegrateUnion, self).__init__(parent)
		self.working = True
		self.num = 0
		self.host=host
		self.port=port
		self.dbNameList=dbNameList
		self.dbName=dbName
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		Integrate.IntegrateUnion(self.host,self.port,self.dbNameList,self.dbName)	
		self.sinOut.emit('end')
		
class LoadingWindowIntegrateTable(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,host,port,dbNameList,dbName,makeDbName):
		super(LoadingWindowIntegrateTable, self).__init__()
		self.host=host
		self.port=port
		self.dbNameList=dbNameList
		self.dbName=dbName
		self.makeDbName=makeDbName
		self.thread = WorkerIntegrateTable(host,port,dbNameList,dbName,makeDbName)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowPCL):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerIntegrateTable(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,host,port,dbNameList,dbName,makeDbName,parent=None):
		super(WorkerIntegrateTable, self).__init__(parent)
		self.working = True
		self.num = 0
		self.host=host
		self.port=port
		self.dbNameList=dbNameList
		self.dbName=dbName
		self.makeDbName=makeDbName
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		Integrate.IntegrateTable(self.host,self.port,self.dbNameList,self.dbName,self.makeDbName)	
		self.sinOut.emit('end')
class LoadingWindowRC(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,host,port,dbName,dir_choose):
		super(LoadingWindowRC, self).__init__()
		self.host=host
		self.port=port
		self.dbName=dbName
		self.dir_choose=dir_choose
		self.thread = WorkerRC(host,port,dbName,dir_choose)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowPCL):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerRC(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,host,port,dbName,dir_choose,parent=None):
		super(WorkerRC, self).__init__(parent)
		self.working = True
		self.num = 0
		self.host=host
		self.port=port
		self.dbName=dbName
		self.dir_choose=dir_choose
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		PS_RC.RC(self.host,self.port,self.dbName,self.dir_choose)	
		self.sinOut.emit('end')	
class LoadingWindowPPD(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,host,port,dbName,dir_choose):
		super(LoadingWindowPPD, self).__init__()
		self.host=host
		self.port=port
		self.dbName=dbName
		self.dir_choose=dir_choose
		self.thread = WorkerPPD(host,port,dbName,dir_choose)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowPCL):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerPPD(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,host,port,dbName,dir_choose,parent=None):
		super(WorkerPPD, self).__init__(parent)
		self.working = True
		self.num = 0
		self.host=host
		self.port=port
		self.dbName=dbName
		self.dir_choose=dir_choose
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		PS_PPD.PPD(self.host,self.port,self.dbName,self.dir_choose)		

		self.sinOut.emit('end')	
class LoadingWindowPCL(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,host,port,dbName,dir_choose,L_check):
		super(LoadingWindowPCL, self).__init__()
		self.host=host
		self.port=port
		self.dbName=dbName
		self.dir_choose=dir_choose
		self.L_check=L_check
		self.thread = WorkerPCL(host,port,dbName,dir_choose,L_check)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowPCL):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerPCL(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,host,port,dbName,dir_choose,L_check,parent=None):
		super(WorkerPCL, self).__init__(parent)
		self.working = True
		self.num = 0
		self.host=host
		self.port=port
		self.dbName=dbName
		self.L_check=L_check
		self.dir_choose=dir_choose
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		collect_all.collect(self.host,self.port,self.dbName,self.dir_choose,self.L_check)		

		self.sinOut.emit('end')	
		
		
class LoadingWindowIddIds(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,path_old,path_new,listName,fileName,path_biaozhun,typeName,replay):
		super(LoadingWindowIddIds, self).__init__()
		self.path_old=path_old
		self.path_new=path_new
		self.listName=listName
		self.fileName=fileName
		self.path_biaozhun=path_biaozhun
		self.typeName=typeName
		self.replay=replay
		self.thread = WorkerIddIds(path_old,path_new,listName,fileName,path_biaozhun,typeName,replay)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowIddIds):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerIddIds(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,path_old,path_new,listName,fileName,path_biaozhun,typeName,replay, parent=None):
		super(WorkerIddIds, self).__init__(parent)
		self.working = True
		self.num = 0
		self.path_old=path_old
		self.path_new=path_new
		self.listName=listName
		self.fileName=fileName
		self.path_biaozhun=path_biaozhun
		self.typeName=typeName
		self.replay=replay
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
	
#def copyFile(path_old,path_new,listName,fileName,path_biaozhun,typeName,replay):
	# huanchun_list=os.listdir(u"%s\Localize"%(path_old))
	# fileName=[item for item in huanchun_list if item !='Common']
		if self.typeName=='idd':
			CJK=['JPN','CHS','CHT','KOR']
			for txtName in self.listName:
				for lanName in self.fileName:
					print(self.path_old)
					print(self.path_new)
					oldname=u'%s/Localize/%s/Dialog/%s'%(self.path_old,lanName,txtName)
					newFile=u'%s/Localize/%s/Dialog'%(self.path_new,lanName)
					newname=u'%s/Localize/%s/Dialog/%s'%(self.path_new,lanName,txtName)
					if os.path.exists(newFile):
						shutil.copyfile(oldname,newname)
					else:
						os.makedirs(newFile)
						shutil.copyfile(oldname,newname)
					dialog_xml.nodeAdd(txtName,lanName,newname,self.path_biaozhun)
					dialog_xml.paixu(txtName,lanName,newname,self.path_biaozhun)
					dialog_xml.dialog_change(host,port,userdb,passwdb,db,txtName,lanName,newname)
					if lanName in CJK:
						CJKAdd.CJKAdd(txtName,lanName,newname,self.path_biaozhun)
					else:
						shortcutAdd.shortAdd(txtName,lanName,newname,self.path_biaozhun)
					biaodian.biaodian(newname)
			for txtName in NewName:
				for lanName in self.fileName:				
					oldname=u'%s/%s'%(self.path_biaozhun,txtName)
					newFile=u'%s/Localize/%s/Dialog'%(self.path_new,lanName)
					l=(self.path_biaozhun).split('/')[:-2]
					#self.path_new="\\".join(dir_choose_1)
					new_path="/".join(l)
					print(type(l))
					print(new_path)
					newname=u'%s/%s/Dialog/%s'%(new_path,lanName,txtName)
					if os.path.exists(newFile):
						shutil.copyfile(oldname,newname)
					else:
						os.makedirs(newFile)
						shutil.copyfile(oldname,newname)
					dialog_xml.dialog_new(host,port,userdb,passwdb,db,txtName,lanName,newname)
					if lanName in CJK:
						CJKshortcut.CJKshortcut(txtName,lanName,newname,self.path_biaozhun)
					else:
						shortcut.shortcut(txtName,lanName,newname,self.path_biaozhun)
					biaodian.biaodian(newname)
		elif self.typeName=='ids':
			for lanName in self.fileName:
				oldname=u'%s/Localize/%s/StringDefinition.xml'%(self.path_old,lanName)
				newFile=u'%s/%s'%(self.path_biaozhun,lanName)
				bianzhunTxt=u'%s/StringDefinition.xml'%(ids_path_new)
				newname=u'%s/%s/StringDefinition.xml'%(self.path_biaozhun,lanName)
				if os.path.exists(newFile):
					shutil.copyfile(oldname,newname)
				else:
					os.makedirs(newFile)
					shutil.copyfile(oldname,newname)
				IDS.stringDefinition(host,port,userdb,passwdb,db,lanName,bianzhunTxt,newname,self.replay)
				biaodian.biaodian(newname)
		self.sinOut.emit('end')

class LoadingWindowHhcHhk(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,L_check,hhchhkbiaozhun_path,hhchhkshengchen_path,hhchhkName):
		super(LoadingWindowHhcHhk, self).__init__()
		self.L_check=L_check
		self.hhchhkbiaozhun_path=hhchhkbiaozhun_path
		self.hhchhkshengchen_path=hhchhkshengchen_path
		self.hhchhkName=hhchhkName
		self.thread = WorkerHhcHhk(L_check,hhchhkbiaozhun_path,hhchhkshengchen_path,hhchhkName)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowIddIds):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerHhcHhk(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,L_check,hhchhkbiaozhun_path,hhchhkshengchen_path,hhchhkName,parent=None):
		super(WorkerHhcHhk, self).__init__(parent)
		self.working = True
		self.num = 0
		self.L_check=L_check
		self.hhchhkbiaozhun_path=hhchhkbiaozhun_path
		self.hhchhkshengchen_path=hhchhkshengchen_path
		self.hhchhkName=hhchhkName
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		for lanName in self.L_check:
			hhcname='%s.hhc'%(self.hhchhkName)
			hhc_shengcheng.hhc(host,port,userdb,passwdb,db,lanName,self.hhchhkshengchen_path,self.hhchhkbiaozhun_path,hhcname)
			hhkname='%s.hhk'%(self.hhchhkName)
			hhk_shengcheng.hhk(host,port,userdb,passwdb,db,lanName,self.hhchhkshengchen_path,self.hhchhkbiaozhun_path,hhkname)
		self.sinOut.emit('end')	
class LoadingWindowHelp(QDialog):
	"""docstring for LoadingWindowIddIds"""
	def __init__(self,L_check,helpNewName,helpshengchen_path,helpbianzhun_path):
		super(LoadingWindowHelp, self).__init__()
		self.L_check=L_check
		self.helpNewName=helpNewName
		self.helpshengchen_path=helpshengchen_path
		self.helpbianzhun_path=helpbianzhun_path
		self.thread = WorkerHelp(L_check,helpNewName,helpshengchen_path,helpbianzhun_path)
		#self.setupUi(self)

	#def setupUi(self,LoadingWindowIddIds):
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(0, 10, 411, 281))
		self.label.setObjectName("label")
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		movie = QtGui.QMovie("./waiting.gif")
		movie.setCacheMode(QtGui.QMovie.CacheAll)
		movie.setSpeed(100)
		self.label.setMovie(movie)
		movie.start()
		self.slotStart()
		self.thread.sinOut.connect(self.close)
	def slotStart(self):
		#开始按钮不可点击，线程开始
		#self.btnStart.setEnabled(False)
		self.thread.start()
class WorkerHelp(QThread):
	sinOut = pyqtSignal(str)
	def __init__(self,L_check,helpNewName,helpshengchen_path,helpbianzhun_path,parent=None):
		super(WorkerHelp, self).__init__(parent)
		self.working = True
		self.num = 0
		self.L_check=L_check
		self.helpNewName=helpNewName
		self.helpshengchen_path=helpshengchen_path
		self.helpbianzhun_path=helpbianzhun_path
		
	def __del__(self):
		#线程状态改变与线程终止
		self.working = False
		self.wait()
		
	def run(self):
		for lanName in self.L_check:
			for txtName in self.helpNewName:
				help_xingui_tihuan.help_xingui(host,port,userdb,passwdb,db,lanName,txtName,self.helpshengchen_path,self.helpbianzhun_path)
		self.sinOut.emit('end')
def queryLan(lan,wordTxt,laned,hostdb=host,portdb=port,userdb='root',passwdb='123456',dbname=db,tablename=table):
	conn = pymysql.connect(host=host,port=port,user=userdb,passwd=passwdb,db=dbname)
	cursor = conn.cursor()
	sql="SELECT %s from %s where %s='%s'"%(lan,tablename,laned,wordTxt)
	#print(sql)
	cursor.execute(sql) 
	conn.commit() 
	urlData = cursor.fetchall()
	#print(urlData)
	return(urlData)

class MainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.cwd = os.getcwd()
		self.tabWidget = QTabWidget()
		self.setCentralWidget(self.tabWidget)
		fileNewAction = self.createAction("&New", self.fileNew,
				QKeySequence.New, "filenew", "Create a text file")
		fileOpenAction = self.createAction("&Open...", self.fileOpen,
				QKeySequence.Open, "fileopen",
				"Open an existing text file")
		fileSaveAction = self.createAction("&Save", self.fileSave,
				QKeySequence.Save, "filesave", "Save the text")
		fileSaveAsAction = self.createAction("Save &As...",
				self.fileSaveAs, icon="filesaveas",
				tip="Save the text using a new filename")
		fileSaveAllAction = self.createAction("Save A&ll",
				self.fileSaveAll, icon="filesave",
				tip="Save all the files")
		fileCloseTabAction = self.createAction("Close &Tab",
				self.fileCloseTab, QKeySequence.Close, "filequit",
				"Close the active tab")
		fileQuitAction = self.createAction("&Quit", self.close,
				"Ctrl+Q", "filequit", "Close the application")
		editCopyAction = self.createAction("&Copy", self.editCopy,
				QKeySequence.Copy, "editcopy",
				"Copy text to the clipboard")
		editCutAction = self.createAction("Cu&t", self.editCut,
				QKeySequence.Cut, "editcut",
				"Cut text to the clipboard")
		editPasteAction = self.createAction("&Paste", self.editPaste,
				QKeySequence.Paste, "editpaste",
				"Paste in the clipboard's text")
		QShortcut(QKeySequence.PreviousChild, self, self.prevTab)
		QShortcut(QKeySequence.NextChild, self, self.nextTab)
		fileMenu = self.menuBar().addMenu("&File")
		self.addActions(fileMenu, (fileNewAction, fileOpenAction,
				fileSaveAction, fileSaveAsAction, fileSaveAllAction,
				fileCloseTabAction, None, fileQuitAction))
		editMenu = self.menuBar().addMenu("&Edit")
		self.addActions(editMenu, (editCopyAction, editCutAction,
								   editPasteAction))





		insertTxtAction = self.createAction("&insert by line", self.txtInsert, "insert")
		insertKeyAction = self.createAction("&insert by keyword", self.keyInsert, "insertkey")
		removeTxtAction = self.createAction("&remove by line", self.txtremove, "remove")
		removeKeyAction = self.createAction("&remove by keyword", self.keyRemove, "removekey")
		replaceKeyAction= self.createAction("&replace by keyword", self.keyReplace, "replacekey")
		insertMenu = self.menuBar().addMenu("&inser/remove")
		self.addActions(insertMenu, (insertTxtAction, insertKeyAction, removeTxtAction, removeKeyAction,replaceKeyAction,))	

		newDialogAction = self.createAction("&new dialog", self.slot_btn_chooseDir, "new dialog")		
		newStringDefinitionAction = self.createAction("&new StringDefinition", self.ids_btn_chooseDir, "new StringDefinition")
		newHhcHhkAction = self.createAction("&new HhcHhk", self.hhchhk_btn_chooseDir, "new HhcHhk")		
		newHELPAction = self.createAction("&new HELP", self.help_btn_chooseDir, "new HELP")
		newMenu = self.menuBar().addMenu("&new localize")
		self.addActions(newMenu, (newDialogAction, newStringDefinitionAction, newHhcHhkAction, newHELPAction))

		EfolderAction = self.createAction("&Extract folder_PCL", self.ExtractFolder_btn_chooseDir, "Extract folder")
		EstoreXlsAction=self.createAction("&store xls", self.store_btn_xls, "store xls")
		PSppdAction=self.createAction("&Extract_PS_PPD", self.PSppdFolder_btn_chooseDir, "Extract PS_PPD")
		PSrcAction=self.createAction("&Extract_PS_rc", self.PSrcFolder_btn_chooseDir, "Extract PS_RC")
		IntegrateTableAction=self.createAction("&Integrate Table", self.Integrate_Table, "Integrate Table")
		IntegrateUnionAction=self.createAction("&Integrate Union", self.Integrate_Union, "Integrate Union")
		newMenu = self.menuBar().addMenu("&Extract folder")
		self.addActions(newMenu, (EfolderAction,EstoreXlsAction,PSppdAction,PSrcAction,IntegrateTableAction,IntegrateUnionAction))

		#downDbAction = self.createAction("&down db", self.downDB_btn_chooseDir, "down db(xls)")
		upDbAction = self.createAction("&up db", self.update_btn_chooseDir, "up db(xls)")
		DbSettingAction = self.createAction("&db setting", self.dbSetting, "db setting")
		newMenu = self.menuBar().addMenu("&db")
		self.addActions(newMenu, (upDbAction,DbSettingAction))				
				
		fileToolbar = self.addToolBar("File")
		fileToolbar.setObjectName("FileToolbar")
		self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
									  fileSaveAction))
		editToolbar = self.addToolBar("Edit")
		editToolbar.setObjectName("EditToolbar")
		self.addActions(editToolbar, (editCopyAction, editCutAction,
									  editPasteAction))
									 

		settings = QSettings()
		if settings.value("MainWindow/Geometry") or settings.value("MainWindow/State"):
			self.restoreGeometry(
					QByteArray(settings.value("MainWindow/Geometry")))
			self.restoreState(
					QByteArray(settings.value("MainWindow/State")))

		status = self.statusBar()
		status.setSizeGripEnabled(False)
		status.showMessage("Ready", 5000)
		self.setWindowTitle("Tabbed Text Editor")
		QTimer.singleShot(0, self.loadFiles)
	def dbSetting(self):
		dialog=dbSettingWindow(self)
		dialog.mySignal.connect(self.pr)
		dialog.pushButton.clicked.connect(dialog.close)
		dialog.exec_()
		#dbSettingList=dialog.btnpress()
	def pr(self,connect):
		print(connect)
		try:
			global host,port,userdb,passwdb
			host=connect[0]
			port=int(connect[1])
			userdb=connect[2]
			passwdb=connect[3]
			print(host,port,userdb,passwdb)
			conn = pymysql.connect(host=host,port=port,user=userdb,passwd=passwdb)
			cursor = conn.cursor()
			QMessageBox.information(self, "恭喜",'连接通过', QMessageBox.Ok)							
		except:
			QMessageBox.information(self, "警告",'未连接', QMessageBox.Ok)
		# insertNum=dialog.btnPress2_clicked(pathList)[1]
		# stateNum=dialog.btnPress2_clicked(pathList)[2]
		# laned=dialog.btnPress2_clicked(pathList)[3]

	def createAction(self, text, slot=None, shortcut=None, icon=None,
					 tip=None, checkable=False, signal="triggered()"):
		action = QAction(text, self)
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(":/{0}.png".format(icon)))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			action.triggered.connect(slot)
		if checkable:
			action.setCheckable(True)
		return action

	def txtInsert(self):
		dialog=SecondWindow(self)
		dialog.exec_()
		if self.tabWidget.currentWidget()==None:
			return
		pathList=self.tabWidget.currentWidget().filename.split('/')
		text_orgrin=dialog.btnPress2_clicked(pathList)[0]
		insertNum=dialog.btnPress2_clicked(pathList)[1]
		stateNum=dialog.btnPress2_clicked(pathList)[2]
		laned=dialog.btnPress2_clicked(pathList)[3]
		if insertNum=='':
			pass
		else:
			for i in range(self.tabWidget.count()):
				text=text_orgrin
				textEdit = self.tabWidget.widget(i)
				textList=(textEdit.toPlainText().split('\n'))
				if stateNum==2:
					filename=self.tabWidget.widget(i).filename
					print(filename)
					pathList=filename.split('/')
					for lan in pathList:
						if lan in languageList:
							lanName=lan
						else:
							pass
					tihuan_sta=re.compile(r'\{/(.*?)\/}')
					tihuan_duoyu=tihuan_sta.findall(text)  
					for txt in tihuan_duoyu:
						result=queryLan(lanName,txt,laned)
						if result==():
							QMessageBox.information(self, "警告",'%s语言没有该数据'%(lanName), QMessageBox.Ok)
						else:
							if len(result)>1:
								QMessageBox.information(self, "警告",'语言有%s条该数据，使用第一条'%(len(result)), QMessageBox.Ok)
							text=text.replace('{/%s/}'%(txt),result[0][0])
							print(text)
				else:
					text=text_orgrin									
				textList.insert((int(insertNum)-1),text)
				nowText='\n'.join(textList)
				textEdit.setPlainText('%s'%nowText)

			
	def keyInsert(self):
		if self.tabWidget.currentWidget()==None:
			QMessageBox.information(self, "错误",'请打开一个文档', QMessageBox.Ok)
			return
		dialog=keyInsertWindow(self.tabWidget.currentWidget().toPlainText())
		dialog.exec_()
		pathList=self.tabWidget.currentWidget().filename.split('/')
		print(pathList)
		if dialog.btnPress2_clicked(pathList)==None:
			pass	
		else:
			print(dialog.btnPress2_clicked(pathList))
			text_orgrin=dialog.btnPress2_clicked(pathList)[0]
			keyWord=dialog.btnPress2_clicked(pathList)[1]
			insertNum=dialog.btnPress2_clicked(pathList)[3]
			stateNum=dialog.btnPress2_clicked(pathList)[4]
			laned=dialog.btnPress2_clicked(pathList)[5]
			for i in range(self.tabWidget.count()):
				textEdit = self.tabWidget.widget(i)
				textList=(textEdit.toPlainText().split('\n'))
				print(textList)
				txtNum=[]
				for txtLine in textList:
					if keyWord in txtLine:
						txtNum.append(textList.index(txtLine))
				if len(txtNum)==0:
					QMessageBox.information(self, "警告",'当前文档没有该文言', QMessageBox.Ok)
				elif len(txtNum)==1:
					if dialog.btnPress2_clicked(pathList)[2]==True:


						insertTxt=text_orgrin
						if stateNum==2:
							filename=self.tabWidget.widget(i).filename
							print(filename)
							pathList=filename.split('/')
							for lan in pathList:
								if lan in languageList:
									lanName=lan
								else:
									pass
							tihuan_sta=re.compile(r'\{/(.*?)\/}')
							tihuan_duoyu=tihuan_sta.findall(insertTxt)  
							for txt in tihuan_duoyu:
								result=queryLan(lanName,txt,laned)
								if result==():
									QMessageBox.information(self, "警告",'%s语言没有该数据'%(lanName), QMessageBox.Ok)
								else:
									if len(result)>1:
										QMessageBox.information(self, "警告",'语言有%s条该数据，使用第一条'%(len(result)), QMessageBox.Ok)
									insertTxt=insertTxt.replace('{/%s/}'%(txt),result[0][0])
									print(insertTxt)
						else:
							insertTxt=text_orgrin
					
					
						textList.insert((int(txtNum[0])-int(insertNum)+1),insertTxt)
						nowText='\n'.join(textList)
						textEdit.setPlainText('%s'%nowText)
					else:
						insertTxt=text_orgrin
						if stateNum==2:
							filename=self.tabWidget.widget(i).filename
							print(filename)
							pathList=filename.split('/')
							for lan in pathList:
								if lan in languageList:
									lanName=lan
								else:
									pass
							tihuan_sta=re.compile(r'\{/(.*?)\/}')
							tihuan_duoyu=tihuan_sta.findall(insertTxt)  
							for txt in tihuan_duoyu:
								result=queryLan(lanName,txt,laned)
								if result==():
									QMessageBox.information(self, "警告",'%s语言没有该数据'%(lanName), QMessageBox.Ok)
								else:
									if len(result)>1:
										QMessageBox.information(self, "警告",'语言有%s条该数据，使用第一条'%(len(result)), QMessageBox.Ok)
									insertTxt=insertTxt.replace('{/%s/}'%(txt),result[0][0])
									print(insertTxt)
						else:
							insertTxt=text_orgrin
						textList.insert((int(insertNum)+int(txtNum[0])),insertTxt)
						nowText='\n'.join(textList)
						textEdit.setPlainText('%s'%nowText)
				else:
					QMessageBox.information(self, "警告",'当前文档有%s处，请使用唯一标识'%(len(txtNum)), QMessageBox.Ok)

	def keyReplace(self):
		if self.tabWidget.currentWidget()==None:
			QMessageBox.information(self, "错误",'请打开一个文档', QMessageBox.Ok)
			return
		dialog=keyReplaceWindow(self.tabWidget.currentWidget().toPlainText())
		dialog.exec_()
		pathList=self.tabWidget.currentWidget().filename.split('/')
		print(pathList)
		if dialog.btnPress2_clicked(pathList)==None:
			pass	
		else:
			print(dialog.btnPress2_clicked(pathList))
			textOld=dialog.btnPress2_clicked(pathList)[0]
			textNew=dialog.btnPress2_clicked(pathList)[1]
			stateNum=dialog.btnPress2_clicked(pathList)[2]
			laned=dialog.btnPress2_clicked(pathList)[3]
			for i in range(self.tabWidget.count()):
				textEdit = self.tabWidget.widget(i)
				textList=(textEdit.toPlainText().split('\n'))
				print(textList)
				if stateNum==2:
					filename=self.tabWidget.widget(i).filename
					print(filename)
					pathList=filename.split('/')
					for lan in pathList:
						print(lan)
						if lan in languageList:
							lanName=lan
						else:
							pass

					print(lanName)
					resultOld=queryLan(lanName,textOld,laned)
					resultNew=queryLan(lanName,textNew,laned)
					if resultOld==():
						QMessageBox.information(self, "警告",'%s语言没有该数据'%(lanName), QMessageBox.Ok)
					else:
						lineList=[]
						for textLine in textList:
							textLine=textLine.replace(resultOld[0][0],resultNew[0][0])
							lineList.append(textLine)
						print(lineList)
				else:
					filename=self.tabWidget.widget(i).filename
					print(filename)
					pathList=filename.split('/')
					for lan in pathList:
						if lan in languageList:
							lanName=lan
						else:
							pass

					lineList=[]
					for textLine in textList:
						textLine=textLine.replace(textOld,textNew)
						lineList.append(textLine)
					print(lineList)
				
					
					
				nowText='\n'.join(lineList)
				textEdit.setPlainText('%s'%nowText)
			
	def txtremove(self):	
		dialog=RemoveWindow(self)
		dialog.exec_()
		if dialog.btnPress2_clicked()=='':
			pass
		else:
			removeNum=int(dialog.btnPress2_clicked())
			for i in range(self.tabWidget.count()):
				textEdit = self.tabWidget.widget(i)
				textList=(textEdit.toPlainText().split('\n'))
				textList.pop(removeNum-1)
				nowText='\n'.join(textList)
				textEdit.setPlainText('%s'%nowText)
	def keyRemove(self):
		dialog=keyRemoveWindow(self)
		dialog.exec_()
		print(dialog.btnPress2_clicked())
		if dialog.btnPress2_clicked()[0]=='' and dialog.btnPress2_clicked()[2]=='':
			pass
		else:
			keyWord=dialog.btnPress2_clicked()[0]
			removeNum=int(dialog.btnPress2_clicked()[2])
			for i in range(self.tabWidget.count()):
				textEdit = self.tabWidget.widget(i)
				textList=(textEdit.toPlainText().split('\n'))				
				txtNum=[]
				for txtLine in textList:
					if keyWord in txtLine:
						txtNum.append(textList.index(txtLine))
				if len(txtNum)==0:
					QMessageBox.information(self, "警告",'当前文档没有该文言', QMessageBox.Ok)
				elif len(txtNum)==1:
					if dialog.btnPress2_clicked()[1]==True:
						textList.pop(int(txtNum[0])-removeNum)
						nowText='\n'.join(textList)
						textEdit.setPlainText('%s'%nowText)
					else:
						textList.pop(removeNum+int(txtNum[0]))
						nowText='\n'.join(textList)
						textEdit.setPlainText('%s'%nowText)						
				else:
					QMessageBox.information(self, "警告",'当前文档有%s处，请使用唯一标识'%(len(txtNum)), QMessageBox.Ok)				
	def addActions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)

	def closeEvent(self, event):
		failures = []
		for i in range(self.tabWidget.count()):
			textEdit = self.tabWidget.widget(i)
			if textEdit.isModified():
				try:
					textEdit.save()
				except IOError as e:
					failures.append(str(e))
		if (failures and
			QMessageBox.warning(self, "Text Editor -- Save Error",
					"Failed to save{0}\nQuit anyway?".format(
					"\n\t".join(failures)),
					QMessageBox.Yes|QMessageBox.No) ==
					QMessageBox.No):
			event.ignore()
			return
		settings = QSettings()
		settings.setValue("MainWindow/Geometry",
						  self.saveGeometry())
		settings.setValue("MainWindow/State",
						  self.saveState())
		files = []
		for i in range(self.tabWidget.count()):
			textEdit = self.tabWidget.widget(i)
			if not textEdit.filename.startswith("Unnamed"):
				files.append(textEdit.filename)
		settings.setValue("CurrentFiles", files)
		while self.tabWidget.count():
			textEdit = self.tabWidget.widget(0)
			textEdit.close()
			self.tabWidget.removeTab(0)


	def prevTab(self):
		last = self.tabWidget.count()
		current = self.tabWidget.currentIndex()
		if last:
			last -= 1
			current = last if current == 0 else current - 1
			self.tabWidget.setCurrentIndex(current)
	def nextTab(self):
		last = self.tabWidget.count()
		current = self.tabWidget.currentIndex()
		if last:
			last -= 1
			current = 0 if current == last else current + 1
			self.tabWidget.setCurrentIndex(current)


	def loadFiles(self):
		if len(sys.argv) > 1:
			count = 0
			for filename in sys.argv[1:]:
				if QFileInfo(filename).isFile():
					self.loadFile(filename)
					QApplication.processEvents()
					count += 1
					if count >= 10: # Load at most 10 files
						break
		else:
			settings = QSettings()
			#files = settings.value("CurrentFiles").toStringList()
			if settings.value("CurrentFiles"):
				files=settings.value("CurrentFiles")
				for filename in files:
					filename = filename
					if QFile.exists(filename):
						self.loadFile(filename)
						QApplication.processEvents()


	def fileNew(self):
		textEdit = textedit.TextEdit()
		self.tabWidget.addTab(textEdit, textEdit.windowTitle())
		self.tabWidget.setCurrentWidget(textEdit)
	def fileOpen(self):
		filename,filetype = QFileDialog.getOpenFileName(self,
				"Tabbed Text Editor -- Open File")
		pathList=filename.split('/')
		lanSum=0
		for lan in pathList:
			if lan in languageList:
				lanSum+=1
				lanName=lan
			else:
				pass
		if lanSum==1:
			pathNum=pathList.index(lanName)
		else:
			return
		openlist=[]
		filePath='/'.join(pathList[:pathNum])
		#print(os.listdir(filePath))
		
		global chooseFileName
		chooseFileName=[item for item in os.listdir(filePath) if item in languageList]
		#self.haoN=checkboxList(chooseFileName)
		#self.haoN.show()
		dialog=checkboxList(self)
		dialog.exec_()
		languageList_Choose=(dialog.go())
		
		
		for lan in languageList_Choose:
			pathList[pathNum]=lan
			s='/'.join(pathList)
			openlist.append(s)
		#print(openlist)
			
		
		
		#print(self.tabWidget.count())
		#filename=r'C:/Users/Xuexiaobo/Desktop/xiugai/text/resources.qrc'
		if filename:
			#self.tabWidget.addTab(textEdit, textEdit.windowTitle())
			for i in range(self.tabWidget.count()):
				#print(i)
				textEdit = self.tabWidget.widget(i)
				#print(textEdit.filename)
				if textEdit.filename == filename:
					self.tabWidget.setCurrentWidget(textEdit)
					#print('1')
					break
			else:
				#print('load')
				try:
					#print(filename)
					openlist.remove(filename)
					openlist.append(filename)
				except:
				   pass
				for lanName in openlist:
					self.loadFile(lanName)


	def loadFile(self, filename,lan=None):
		textEdit = textedit.TextEdit(filename)
		try:
			textEdit.load()
		except EnvironmentError as e:
			QMessageBox.warning(self,
					"Tabbed Text Editor -- Load Error",
					"Failed to load {0}: {1}".format(filename, e))
			textEdit.close()
			del textEdit
		else:
			txtList=filename.split('/')
			for lan in txtList:
				if lan in languageList:
					lanName=lan
			#print(type(textEdit.windowTitle()))
			self.tabWidget.addTab(textEdit, ('%s-%s')%(lanName,textEdit.windowTitle()))
			self.tabWidget.setCurrentWidget(textEdit)

	def fileSave(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return True
		try:
			textEdit.save()
			#textEdit.setPlainText('11')
			#print(QFileInfo(textEdit.filename).fileName())
			#print(self.tabWidget.currentWidget().toPlainText())
			#print(dir(QFileInfo(textEdit.filename)))
			#print(dir(textEdit.document))
			#print(textEdit.document)
			#print(textEdit.filename)		
			#print(self.tabWidget.currentIndex())
			self.tabWidget.setTabText(self.tabWidget.currentIndex(),
					QFileInfo(textEdit.filename).fileName())
			return True
		except EnvironmentError as e:
			QMessageBox.warning(self,
					"Tabbed Text Editor -- Save Error",
					"Failed to save {0}: {1}".format(textEdit.filename, e))
			return False
	def fileSaveAs(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return True
		filename,filetype = QFileDialog.getSaveFileName(self,
				"Tabbed Text Editor -- Save File As", textEdit.filename,
				"Text files (*.txt *.*)")
		if filename:
			textEdit.filename = filename
			return self.fileSave()
		return True


	def fileSaveAll(self):
		errors = []
		for i in range(self.tabWidget.count()):
			textEdit = self.tabWidget.widget(i)
			#if textEdit.isModified():
			try:
				textEdit.save()
			except EnvironmentError as e:
				errors.append("{0}: {1}".format(textEdit.filename, e))
		if errors:
			QMessageBox.warning(self, "Tabbed Text Editor -- "
					"Save All Error",
					"Failed to save\n{0}".format("\n".join(errors)))


	def fileCloseTab(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return
		textEdit.close()
	def editCopy(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return
		cursor = textEdit.textCursor()
		text = cursor.selectedText()
		if text:
			clipboard = QApplication.clipboard()
			clipboard.setText(text)


	def editCut(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return
		cursor = textEdit.textCursor()
		text = cursor.selectedText()
		if text:
			cursor.removeSelectedText()
			clipboard = QApplication.clipboard()
			clipboard.setText(text)


	def editPaste(self):
		textEdit = self.tabWidget.currentWidget()
		if textEdit is None or not isinstance(textEdit, QPlainTextEdit):
			return
		clipboard = QApplication.clipboard()
		textEdit.insertPlainText(clipboard.text())
# class SecondWindow(QMainWindow):
	# def __init__(self):
		# super(SecondWindow, self).__init__()
		# self.newWindowUI()

	# def newWindowUI(self):
		# print(12)
		# self.resize(9,9)
		# self.move(200,200)
	def help_btn_chooseDir(self):

		files, ok1 = QFileDialog.getOpenFileNames(self, "选取新规的HELP文件，如：HELP/Apply.htm", "/", "所有文件 (*);;文本文件 (*.txt)")
		if files == []:
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(files)
		global helpNewName  # 新规
		helpNewName = [item.split('/')[-1] for item in files]
		global helpshengchen_path  # 新规
		global helpbianzhun_path
		helpshengchen_path = '/'.join(files[0].split('/')[:-3])
		helpbianzhun_path = '/'.join(files[0].split('/')[:-1])

		dir_choose = QFileDialog.getExistingDirectory(self,
													  "选取要base文件夹,例如:760",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		global hhchhk_path_old
		help_path_old = dir_choose
		help_huanchun_list = os.listdir(u"%s/Localize/Common/RBK/DP_Generated/HELP" % (help_path_old))
		global fileName
		fileName = [item for item in help_huanchun_list if item != 'Common']
		self.haoN = checkboxListNew('help')
		self.haoN.show()

	def hhchhk_btn_chooseDir(self):

		files, ok1 = QFileDialog.getOpenFileNames(self, "选取要基准文件，如：JPN/HELP_1200.hhc.(hhc,hhk选一个即可)", "/",
												  "所有文件 (*);;文本文件 (*.txt)")
		print(files)
		global hhchhkbiaozhun_path
		global hhchhkshengchen_path  # 新规
		global hhchhkName
		if files == []:
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(files)
		hhchhkbiaozhun_path = '/'.join(files[0].split('/')[:-1])
		hhchhkName = [item.split('/')[-1] for item in files][0].split('.')[0]
		hhchhkshengchen_path = '/'.join(files[0].split('/')[:-2])
		print(hhchhkbiaozhun_path)

		dir_choose = QFileDialog.getExistingDirectory(self,
													  "选取要base文件夹,例如:760",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		global hhchhk_path_old
		hhchhk_path_old = dir_choose
		hhchhk_huanchun_list = os.listdir(u"%s/Localize/Common/RBK/DP_Generated/HELP" % (hhchhk_path_old))
		global fileName
		fileName = [item for item in hhchhk_huanchun_list if item != 'Common']
		self.haoN = checkboxListNew('hhchhk')
		self.haoN.show()

	def ids_btn_chooseDir(self):

		dir_choose = QFileDialog.getExistingDirectory(self,
													  "选取要基准文件夹,例如:JPN",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		global ids_path_new
		global ids_path_biaozhun
		l = (dir_choose).split('/')[:-1]
		print(l)
		ids_path_biaozhun = "/".join(l)
		ids_path_new = dir_choose
		dir_choose = QFileDialog.getExistingDirectory(self,
													  "选取要base文件夹,例如:760",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		global ids_path_old
		ids_path_old = dir_choose
		ids_huanchun_list = os.listdir(u"%s/Localize" % (ids_path_old))
		global fileName
		fileName = [item for item in ids_huanchun_list if item != 'Common']
		self.haoN = checkboxListNew('ids')
		self.haoN.show()

	def slot_btn_chooseDir(self):

		dir_choose = QFileDialog.getExistingDirectory(self,
													  "选取要基准文件夹,例如:JPN\Dialog",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		global path_new
		global path_biaozhun
		l = (dir_choose).split('/')[:-3]
		print(l)
		path_new = "/".join(l)
		print(type(l))
		print(path_new)
		path_biaozhun = dir_choose

		files, ok1 = QFileDialog.getOpenFileNames(self, "新规多文件选择", "/", "所有文件 (*);;文本文件 (*.txt)")
		print(files)
		global NewName  # 新规
		NewName = [item.split('/')[-1] for item in files]
		files, ok1 = QFileDialog.getOpenFileNames(self, " 留用多文件(包括留用修改的)选择", "/", "所有文件 (*);;文本文件 (*.txt)")
		print(files)
		global listName  # 留用(包括修改)
		listName = [item.split('/')[-1] for item in files]

		dir_choose = QFileDialog.getExistingDirectory(self,
													  "你选择要base文件夹为:",
													  self.cwd)  # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择要复制到的文件夹为:")
		print(dir_choose)
		global path_old
		path_old = dir_choose
		huanchun_list = os.listdir(u"%s\Localize" % (path_old))
		global fileName
		fileName = [item for item in huanchun_list if item != 'Common']
		self.haoN = checkboxListNew('idd')
		self.haoN.show()

	def downDB_btn_chooseDir(self):
		try:
			store_xls.store_xls(dbName=db,tableNameList=[table])
			QApplication.processEvents()
			QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError, IndexError, PermissionError)  as e:
			print(e)
			return
			#QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)


	def update_btn_chooseDir(self):
		files, ok1 = QFileDialog.getOpenFileNames(self, "选取要上传的模板.xls", "/", "所有文件 (*);;文本文件 (*.txt)")
		try:
			excelToMysql.eToM(host,port,files[0],db)
			QApplication.processEvents()
			QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError, IndexError, PermissionError)  as e:
			print(e)
			return
			#QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)
	def ExtractFolder_btn_chooseDir(self):
		dialog=dbNameWindow(self)
		dialog.mySignal.connect(self.prFolder)
		dialog.pushButton.clicked.connect(dialog.close)
		dialog.show()
	def prFolder(self,connect):
		dbName=connect[0]
		dir_choose = QFileDialog.getExistingDirectory(self,  
									"选取文件夹",  
									self.cwd) # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		self.haoN = checkboxListType(dbName,dir_choose)
		self.haoN.show()			


	def PSppdFolder_btn_chooseDir(self):
		dialog=dbNameWindow(self)
		dialog.mySignal.connect(self.prPpd)
		dialog.pushButton.clicked.connect(dialog.close)
		dialog.exec_()
	def prPpd(self,connect):
		dbName=connect[0]
		dir_choose = QFileDialog.getExistingDirectory(self,  
									"选取文件夹",  
									self.cwd) # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		try:
			#PS_PPD.PPD(host,port,dbName,dir_choose)
			dialog=LoadingWindowPPD(host,port,dbName,dir_choose)
			dialog.exec_()
			QApplication.processEvents()
			QMessageBox.information(self, "提示",'抽取完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)
	def Integrate_Table(self):
		dialog=dbTree(self)
		dialog.mySignal.connect(self.InTable)
		dialog.bt.clicked.connect(dialog.close)
		dialog.exec_()
	def InTable(self,connect):	
		self.dbNameList=connect
		dialog=dbListWindow(self)
		dialog.mySignal.connect(self.InTable2)
		dialog.bt.clicked.connect(dialog.close)
		dialog.exec_()
	def InTable2(self,connect):	
		self.dbName=connect[0]
		dialog=dbNameWindow(self)
		dialog.mySignal.connect(self.InTable3)
		dialog.pushButton.clicked.connect(dialog.close)
		dialog.exec_()			
	def InTable3(self,connect):
		makeDbName=connect[0]
		#print(dbName)
		try:
			dialog=LoadingWindowIntegrateTable(host,port,self.dbNameList,self.dbName,makeDbName)
			dialog.exec_()			
			#Integrate.IntegrateTable(host,port,dbName)
			QApplication.processEvents()
			QMessageBox.information(self, "提示",'合并完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)

	def Integrate_Union(self):
		dialog=dbCheckWindow(self)
		dialog.mySignal.connect(self.InUnion)
		dialog.bt.clicked.connect(dialog.close)
		dialog.exec_()
	def InUnion(self,connect):	
		self.dbNameList=connect
		dialog=dbListWindow(self)
		dialog.mySignal.connect(self.InUnion2)
		dialog.bt.clicked.connect(dialog.close)
		dialog.exec_()		
	
	def InUnion2(self,connect):
		dbName=connect[0]
		print(self.dbNameList)
		try:
			dialog=LoadingWindowIntegrateUnion(host,port,self.dbNameList,dbName)
			dialog.exec_()			
			#Integrate.IntegrateTable(host,port,dbName)
			QApplication.processEvents()
			QMessageBox.information(self, "提示",'合并完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)
		
			
	def PSrcFolder_btn_chooseDir(self):
		dialog=dbNameWindow(self)
		dialog.mySignal.connect(self.prRc)
		dialog.pushButton.clicked.connect(dialog.close)
		dialog.exec_()
	def prRc(self,connect):
		dbName=connect[0]
		dir_choose = QFileDialog.getExistingDirectory(self,  
									"选取文件夹",  
									self.cwd) # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		try:
			#PS_RC.RC(host,port,dbName,dir_choose)
			dialog=LoadingWindowRC(host,port,dbName,dir_choose)
			dialog.exec_()
			QApplication.processEvents()
			QMessageBox.information(self, "提示",'抽取完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)
			
			
	def store_btn_xls(self):
		dialog=dbTree(self)
		dialog.mySignal.connect(self.pr1)
		dialog.bt.clicked.connect(dialog.close)
		dialog.exec_()
	def pr1(self,connect):
		dbNameList=connect
		dir_choose = QFileDialog.getExistingDirectory(self,  
									"选取文件夹",  
									self.cwd) # 起始路径

		if dir_choose == "":
			print("\n取消选择")
			return

		print("\n你选择的文件夹为:")
		print(dir_choose)
		try:
			collect_all.storeXls(host,port,dbNameList,dir_choose)
			QApplication.processEvents()
			QMessageBox.information(self, "提示",'转换完成了', QMessageBox.Yes | QMessageBox.No)
		except (NameError,IndexError,PermissionError)  as e:
			print(e)
			QMessageBox.information(self, "error",  str(e), QMessageBox.Yes | QMessageBox.No)	
			
class checkboxListNew(QWidget):

	def __init__(self, typeName):
		super().__init__()
		self.initUI()
		self.typeName = typeName

	def initUI(self):
		# 新建4个复选框对象

		# lpostion=['50','80','110','140','170','200','230','260','290','320','350','380','410','440','470','500','530','560','590','620','650','680','710','740','770']
		l = fileName
		sum = 0
		for nameNum in range(len(fileName)):
			n = setattr(self, "cb%d" % nameNum, QCheckBox('%s' % (fileName[nameNum]), self))
			m = getattr(self, "cb%d" % nameNum)
			m.move(30, textpostion(nameNum))
			sum = max(sum, textpostion(nameNum))
		# button.setFixedSize(QtCore.QSize(60,30))
		self.qxbtn = QCheckBox('all', self)
		# m=getattr(self,"cb%d"%pipe)
		# self.cb1 = QCheckBox('%s'%(l[0]),self)
		# self.cb2 = QCheckBox('%s'%(l[1]),self)
		# self.cb3 = QCheckBox('我的',self)
		# self.cb4 = QCheckBox('宝贝',self)

		bt = QPushButton('提交', self)

		self.resize(300, sum + 100)
		self.setWindowTitle('选择要复制的文件夹')

		self.qxbtn.move(20, 20)
		# self.cb2.move(30,50)
		# self.cb3.move(30,80)
		# self.cb4.move(30,110)

		bt.move(20, sum + 50)

		self.qxbtn.stateChanged.connect(self.changecb1)
		# self.cb2.stateChanged.connect(self.changecb2)
		# self.cb3.stateChanged.connect(self.changecb2)
		# self.cb4.stateChanged.connect(self.changecb2)
		bt.clicked.connect(self.go)
		bt.clicked.connect(self.close)

		self.show()

	def go(self):
		L_check = []
		for pipe in range(len(fileName)):
			m = getattr(self, "cb%d" % pipe)
			if m.isChecked():
				# print("pipe"),
				L_check.append(fileName[pipe])
			# print(pipe),
			# print("is selected!!!")
		print(L_check)
		if self.typeName == 'idd':
			try:
				dialog=LoadingWindowIddIds(path_old,path_new,listName,L_check,path_biaozhun,self.typeName,None)
				dialog.exec_()
				QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
			except (NameError, IndexError, PermissionError)  as e:
				print(e)
				QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)
		elif self.typeName == 'ids':
			replay = QMessageBox.information(self, "选择", '是否和标准格式保持严格一致(严格按照标准的ids)', QMessageBox.Yes | QMessageBox.No)
			print(replay)
			# if replay!=int(16384):
			try:
				dialog=LoadingWindowIddIds(ids_path_old, ids_path_new, None, L_check, ids_path_biaozhun, self.typeName, replay)
				dialog.exec_()
				QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
			except (NameError, IndexError, PermissionError)  as e:
				print(e)
				QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)
		elif self.typeName == 'hhchhk':

			try:
				dialog=LoadingWindowHhcHhk(L_check, hhchhkbiaozhun_path, hhchhkshengchen_path, hhchhkName)
				dialog.exec_()
				QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
			except (NameError, IndexError, PermissionError)  as e:
				print(e)
				QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)

		elif self.typeName == 'help':
			try:

				dialog=LoadingWindowHelp(L_check, helpNewName, helpshengchen_path, helpbianzhun_path)
				dialog.exec_()
				QMessageBox.information(self, "提示", '复制完成了', QMessageBox.Yes | QMessageBox.No)
			except (NameError, IndexError, PermissionError)  as e:
				print(e)
				QMessageBox.information(self, "error", str(e), QMessageBox.Yes | QMessageBox.No)

	def changecb1(self):
		if self.qxbtn.checkState() == Qt.Checked:
			for nameNum in range(len(fileName)):
				m = getattr(self, "cb%d" % nameNum)
				m.setChecked(True)
		elif self.qxbtn.checkState() == Qt.Unchecked:
			for nameNum in range(len(fileName)):
				m = getattr(self, "cb%d" % nameNum)
				m.setChecked(False)

	def changecb2(self):
		if self.cb2.isChecked() and self.cb3.isChecked() and self.cb4.isChecked():
			self.cb1.setCheckState(Qt.Checked)
		elif self.cb2.isChecked() or self.cb3.isChecked() or self.cb4.isChecked():
			self.cb1.setTristate()
			self.cb1.setCheckState(Qt.PartiallyChecked)
		else:
			self.cb1.setTristate(False)
			self.cb1.setCheckState(Qt.Unchecked)




def textpostion(i):
	return(50+i*30)
class checkboxList(QDialog):

	def __init__(self,parent=None):
		super(checkboxList,self).__init__(parent)
		#self.initUI()


	
	#def initUI(self):
		#新建4个复选框对象

		#lpostion=['50','80','110','140','170','200','230','260','290','320','350','380','410','440','470','500','530','560','590','620','650','680','710','740','770']
		#print(l)
		sum=0
		for nameNum in range(len(chooseFileName)):
			n=setattr(self,"cb%d"%nameNum,QCheckBox('%s'%(chooseFileName[nameNum]),self))
			m=getattr(self,"cb%d"%nameNum)
			m.move(30,textpostion(nameNum))
			sum=max(sum,textpostion(nameNum))
		self.qxbtn=QCheckBox('all',self)

		bt=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		bt.accepted.connect(self.accept)
		bt.rejected.connect(self.reject)
		self.resize(300,sum+100)
		self.setWindowTitle('选择要复制的文件夹')

		self.qxbtn.move(20,20)
# self.cb2.move(30,50)
# self.cb3.move(30,80)
# self.cb4.move(30,110)

		bt.move(40,sum+50)

		self.qxbtn.stateChanged.connect(self.changecb1)
# self.cb2.stateChanged.connect(self.changecb2)
# self.cb3.stateChanged.connect(self.changecb2)
# self.cb4.stateChanged.connect(self.changecb2)
		#bt.clicked.connect(self.go)

		#self.show()	
	def go(self):
		L_check=[]
		for pipe in range(len(chooseFileName)):
			m=getattr(self,"cb%d"%pipe)
			if m.isChecked():
				L_check.append(chooseFileName[pipe])
		return (L_check)

				# print("is selected!!!")
		
	def changecb1(self):
		if self.qxbtn.checkState() == Qt.Checked:
			for nameNum in range(len(chooseFileName)):
				m=getattr(self,"cb%d"%nameNum)
				m.setChecked(True)
		elif self.qxbtn.checkState() == Qt.Unchecked:
			for nameNum in range(len(chooseFileName)):
				m=getattr(self,"cb%d"%nameNum)
				m.setChecked(False)		
class SecondWindow(QDialog):
	def __init__(self,parent=None):
		super(SecondWindow, self).__init__(parent)
		
		self.setWindowTitle('自定义窗口')
		self.resize(477, 338)
		self.textEdit=QPlainTextEdit()
		#创建两个按钮
		self.state=0
		layout=QVBoxLayout(self)
		checkBox = QtWidgets.QCheckBox('是否使用语言替换插入', self)
		checkBox.stateChanged.connect(self.checkLanguage)
		# self.btnPress1=QPushButton('插入到第二行')
		# self.btnPress2=QPushButton('取消')
		# self.btnPress2.clicked.connect(self.btnPress2_clicked)

		#相关控件添加到垂直布局中
		self.lineEdit=QLineEdit(self)
		layout.addWidget(self.textEdit)
		layout.addWidget(self.lineEdit)
		buttons=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(checkBox)
		layout.addWidget(buttons)


	# def btnPress1_clicked(self):
		# #以文本的形式输出到多行文本框
		# text=self.textEdit.toPlainText()
		# dialog=MainWindow(self)
		# result=dialog.exec_()
		# date=dialog.dateTime()
		# self.lineEdit.setText(date.date().toString())
	def checkLanguage(self, state):
		checkBox = self.sender()
		if state == QtCore.Qt.Unchecked:
			self.state=state
		elif state == QtCore.Qt.Checked:
			self.state=state
			
	def btnPress2_clicked(self,pathList):
		#以Html的格式输出多行文本框，字体红色，字号6号
		#print('done')
		#print(dir(self.lineEdit))
		#print(self.state)
		
		for lan in pathList:
			if lan in languageList:
				laned=lan
			else:
				pass
		return(self.textEdit.toPlainText(),self.lineEdit.text(),self.state,laned)
class keyReplaceWindow(QDialog):
	def __init__(self,txtWord,parent=None):
		super(keyReplaceWindow, self).__init__(parent)
		
		self.setWindowTitle('自定义窗口')
		self.resize(477, 338)
		self.state=0
		checkBox = QtWidgets.QCheckBox('是否使用语言替换插入', self)
		checkBox.stateChanged.connect(self.checkLanguage)
		self.txt=txtWord
		#创建两个按钮
		layout=QVBoxLayout(self)

		#相关控件添加到垂直布局中
		self.lineEditOld=QLineEdit(self)
		self.lineEditNew=QLineEdit(self)
		layout.addWidget(self.lineEditOld)
		layout.addWidget(self.lineEditNew)
		layout.addWidget(checkBox)
		buttons=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)


	# def btnPress1_clicked(self):
		# #以文本的形式输出到多行文本框
		# text=self.textEdit.toPlainText()
		# dialog=MainWindow(self)
		# result=dialog.exec_()
		# date=dialog.dateTime()
		# self.lineEdit.setText(date.date().toString())
	def checkLanguage(self, state):
		checkBox = self.sender()
		if state == QtCore.Qt.Unchecked:
			self.state=state
		elif state == QtCore.Qt.Checked:
			self.state=state
			
	def btnPress2_clicked(self,pathList):
		#以Html的格式输出多行文本框，字体红色，字号6号
		#print('done')
		#print(dir(self.lineEdit))
		#print(self.lineEdit.text())
		txtList=self.txt.split('\n')
		#print(txtList)
		#print(self.lineEdit.text())
		txtNum=[]
		#print(txtList)
		for txtLine in txtList:
			if self.lineEditOld.text() in txtLine:
				txtNum.append(txtList.index(txtLine))
		#print(len(txtNum))
		if self.lineEditOld.text()=='' and self.lineEditNew.text()=='':
			pass
		else:
			if len(txtNum)==0:
				QMessageBox.information(self, "警告",'当前文档没有该文言', QMessageBox.Ok)
			elif len(txtNum)==1:
				for lan in pathList:
					if lan in languageList:
						laned=lan
					else:
						pass
		#return(self.textEdit.toPlainText(),self.lineEdit.text(),self.state,laned)
				return(self.lineEditOld.text(),self.lineEditNew.text(),self.state,laned)
			else:
				QMessageBox.information(self, "警告",'当前文档有%s处，请使用唯一标识'%(len(txtNum)), QMessageBox.Ok)

class keyInsertWindow(QDialog):
	def __init__(self,txtWord,parent=None):
		super(keyInsertWindow, self).__init__(parent)
		
		self.setWindowTitle('自定义窗口')
		self.resize(477, 338)
		self.state=0
		checkBox = QtWidgets.QCheckBox('是否使用语言替换插入', self)
		checkBox.stateChanged.connect(self.checkLanguage)
		self.textEdit=QPlainTextEdit()
		self.txt=txtWord
		#创建两个按钮
		layout=QVBoxLayout(self)

		#相关控件添加到垂直布局中
		self.lineEdit=QLineEdit(self)
		self.radioUp = QRadioButton("Up")
		self.radioDown = QRadioButton("Down")
		self.lineEditNum=QLineEdit(self)
		self.radioUp.setChecked(True)
		layout.addWidget(self.textEdit)
		layout.addWidget(self.lineEdit)
		layout.addWidget(self.radioUp)
		layout.addWidget(self.radioDown)
		layout.addWidget(self.lineEditNum)
		layout.addWidget(checkBox)
		buttons=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)


	# def btnPress1_clicked(self):
		# #以文本的形式输出到多行文本框
		# text=self.textEdit.toPlainText()
		# dialog=MainWindow(self)
		# result=dialog.exec_()
		# date=dialog.dateTime()
		# self.lineEdit.setText(date.date().toString())
	def checkLanguage(self, state):
		checkBox = self.sender()
		if state == QtCore.Qt.Unchecked:
			self.state=state
		elif state == QtCore.Qt.Checked:
			self.state=state
			
	def btnPress2_clicked(self,pathList):
		#以Html的格式输出多行文本框，字体红色，字号6号
		#print('done')
		#print(dir(self.lineEdit))
		#print(self.lineEdit.text())
		txtList=self.txt.split('\n')
		#print(txtList)
		#print(self.lineEdit.text())
		txtNum=[]
		#print(txtList)
		for txtLine in txtList:
			if self.lineEdit.text() in txtLine:
				txtNum.append(txtList.index(txtLine))
		#print(len(txtNum))
		if self.textEdit.toPlainText()=='' and self.lineEdit.text()=='':
			pass
		else:
			if len(txtNum)==0:
				QMessageBox.information(self, "警告",'当前文档没有该文言', QMessageBox.Ok)
			elif len(txtNum)==1:
				for lan in pathList:
					if lan in languageList:
						laned=lan
					else:
						pass
		#return(self.textEdit.toPlainText(),self.lineEdit.text(),self.state,laned)
				return(self.textEdit.toPlainText(),self.lineEdit.text(),self.radioUp.isChecked(),self.lineEditNum.text(),self.state,laned)
			else:
				QMessageBox.information(self, "警告",'当前文档有%s处，请使用唯一标识'%(len(txtNum)), QMessageBox.Ok)

class RemoveWindow(QDialog):
	def __init__(self,parent=None):
		super(RemoveWindow, self).__init__(parent)	   
		self.setWindowTitle('输入删除的行数')
		self.resize(200, 100)
		layout=QVBoxLayout(self)
		self.lineEdit=QLineEdit(self)
		layout.addWidget(self.lineEdit)
		buttons=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)
	def btnPress2_clicked(self):
		return(self.lineEdit.text())
class keyRemoveWindow(QDialog):
	def __init__(self,parent=None):
		super(keyRemoveWindow, self).__init__(parent)	   
		self.setWindowTitle('输入删除的关键字，行数')
		self.resize(200, 100)
		layout=QVBoxLayout(self)
		self.lineEdit=QLineEdit(self)
		self.lineEditNum=QLineEdit(self)
		self.radioUp = QRadioButton("Up")
		self.radioDown = QRadioButton("Down")
		self.radioUp.setChecked(True)
		layout.addWidget(self.lineEdit)
		layout.addWidget(self.radioUp)
		layout.addWidget(self.radioDown)
		layout.addWidget(self.lineEditNum)
		buttons=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,Qt.Horizontal,self)
		buttons.accepted.connect(self.accept)
		buttons.rejected.connect(self.reject)
		layout.addWidget(buttons)
	def btnPress2_clicked(self):
		return(self.lineEdit.text(),self.radioUp.isChecked(),self.lineEditNum.text())
class dbSettingWindow(QDialog):
	mySignal = pyqtSignal(list)
	def __init__(self,parent=None):
		super(dbSettingWindow,self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.setObjectName("Form")
		self.resize(400, 300)
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(50, 40, 54, 12))
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(self)
		self.label_2.setGeometry(QtCore.QRect(50, 90, 54, 12))
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(self)
		self.label_3.setGeometry(QtCore.QRect(50, 140, 54, 12))
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(self)
		self.label_4.setGeometry(QtCore.QRect(50, 190, 54, 12))
		self.label_4.setObjectName("label_4")
		self.lineEdit = QtWidgets.QLineEdit(self)
		self.lineEdit.setGeometry(QtCore.QRect(160, 40, 113, 20))
		self.lineEdit.setObjectName("lineEdit")
		self.lineEdit_2 = QtWidgets.QLineEdit(self)
		self.lineEdit_2.setGeometry(QtCore.QRect(160, 90, 113, 20))
		self.lineEdit_2.setObjectName("lineEdit_2")
		self.lineEdit_3 = QtWidgets.QLineEdit(self)
		self.lineEdit_3.setGeometry(QtCore.QRect(160, 140, 113, 20))
		self.lineEdit_3.setObjectName("lineEdit_3")
		self.lineEdit_4 = QtWidgets.QLineEdit(self)
		self.lineEdit_4.setGeometry(QtCore.QRect(160, 190, 113, 20))
		self.lineEdit_4.setObjectName("lineEdit_4")
		self.pushButton = QtWidgets.QPushButton(self)
		self.pushButton.setGeometry(QtCore.QRect(130, 250, 75, 23))
		self.pushButton.setObjectName("pushButton")
		self.setWindowTitle("db setting")
		self.label.setText("host")
		self.label_2.setText("port")
		self.label_3.setText("userName")
		self.label_4.setText("passWord")
		self.pushButton.setText("commit")
		self.pushButton.clicked.connect(self.btnpress)

	def btnpress(self):
		if self.lineEdit.text()!='' and self.lineEdit_2.text()!='' and self.lineEdit_3.text()!='' and self.lineEdit_4.text()!='': 
			self.mySignal.emit([self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text(),self.lineEdit_4.text()]) 
			#self.pushButton.clicked.connect(self.close)			 
		else:
			QMessageBox.information(self, "error",  'please write all the words', QMessageBox.Yes | QMessageBox.No)
		#return(self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text(),self.lineEdit_4.text())
		# self.qxbtn = QCheckBox('all', self)
class dbNameWindow(QDialog):
	mySignal = pyqtSignal(list)
	def __init__(self,parent=None):
		super(dbNameWindow,self).__init__(parent)
		self.setupUi()		
	def setupUi(self):
		self.setObjectName("Form")
		self.resize(335, 194)
		self.lineEdit = QtWidgets.QLineEdit(self)
		self.lineEdit.setGeometry(QtCore.QRect(60, 60, 211, 31))
		self.lineEdit.setObjectName("lineEdit")
		self.pushButton = QtWidgets.QPushButton(self)
		self.pushButton.setGeometry(QtCore.QRect(110, 130, 101, 31))
		self.pushButton.setObjectName("pushButton")
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(60, 20, 131, 31))
		self.label.setObjectName("label")
		self.setWindowTitle("Form")
		self.pushButton.setText("commit")
		self.label.setText("write db/table Name:")
		self.pushButton.clicked.connect(self.btnpress)
	def btnpress(self):
		if self.lineEdit.text()!='': 
			self.mySignal.emit([self.lineEdit.text()]) 
			#self.pushButton.clicked.connect(self.close)			 
		else:
			QMessageBox.information(self, "error",  'please write all the words', QMessageBox.Yes | QMessageBox.No)
def dbNameSearch():
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor = conn.cursor()
	createsql='show databases'
	cursor.execute(createsql)
	conn.commit()	
	data = cursor.fetchall()
	dataList=[item[0] for item in data]
	return(dataList)
class dbListWindow(QDialog):
	mySignal = pyqtSignal(list)
	def __init__(self,parent=None):
		super(dbListWindow,self).__init__(parent)		
		self.setupUi()		
	def setupUi(self):
		self.dataList=dbNameSearch()
		self.setObjectName("Form")
		self.resize(221, 303)
		self.scrollArea = QtWidgets.QScrollArea(self)
		self.scrollArea.setGeometry(QtCore.QRect(9, 9, 201, 251))
		self.scrollArea.setWidgetResizable(False)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 170, len(self.dataList)*30))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		
		
		# self.radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
		# self.radioButton.setGeometry(QtCore.QRect(30, 20, 89, 16))
		# self.radioButton.setObjectName("radioButton")

		for nameNum in range(len(self.dataList)):
			n = setattr(self, "cb%d" % nameNum, QRadioButton('%s' % (self.dataList[nameNum]), self.scrollAreaWidgetContents))
			m = getattr(self, "cb%d" % nameNum)
			m.move(10, textpostion(nameNum)-50)
		
		
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.bt = QtWidgets.QPushButton(self)
		self.bt.setGeometry(QtCore.QRect(70, 270, 75, 23))
		self.bt.setObjectName("pushButton_2")

		self.setWindowTitle("Form")
		# self.radioButton.setText("RadioButton")
		# self.pushButton.setText("PushButton")
		self.bt.setText("确定")
		self.bt.clicked.connect(self.btnpress)
		#bt.clicked.connect(self.close)
		#self.resize(200,500)
		self.show()

	def btnpress(self):
		L_check = []
		for pipe in range(len(self.dataList)):
			m = getattr(self, "cb%d" % pipe)
			if m.isChecked():
				# print("pipe"),
				L_check.append(self.dataList[pipe])
		self.mySignal.emit(L_check)
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
class dbTree(QDialog):
	mySignal = pyqtSignal(list)
	def __init__(self, parent=None):
		super(dbTree, self).__init__(parent)
		self.setWindowTitle('选择要合并的表')
		self.dataList=dbNameSearch()
		self.resize(608, 900)
		self.tree=QTreeWidget(self)
		self.tree.setGeometry(QtCore.QRect(5, 10, 600, 820))	
		self.tree.setColumnCount(1)
		self.tree.setHeaderLabels(['数据库'])
		root=QTreeWidgetItem(self.tree)
		root.setText(0,'Mysql')
		self.tree.setColumnWidth(0,150)
		# child1=QTreeWidgetItem()
		# child1.setText(0,'child1')
		# child1.setCheckState(0,Qt.Unchecked)
		# root.addChild(child1)
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
		self.bt = QtWidgets.QPushButton(self)
		self.bt.setGeometry(QtCore.QRect(110, 850, 75, 31))
		self.bt.setObjectName("pushButton")
		self.bt.setText("确定")
		self.bt.clicked.connect(self.btnpress)	
		self.show()
		#self.tree.clicked.connect(self.onClicked)
		#self.setCentralWidget(self.tree)
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
		self.mySignal.emit(L_check)

class dbCheckWindow(QDialog):
	mySignal = pyqtSignal(list)
	def __init__(self,parent=None):
		super(dbCheckWindow,self).__init__(parent)		
		self.setupUi()		
	def setupUi(self):
		self.dataList=dbNameSearch()
		self.setObjectName("Form")
		self.resize(221, 303)
		self.scrollArea = QtWidgets.QScrollArea(self)
		self.scrollArea.setGeometry(QtCore.QRect(9, 9, 201, 251))
		self.scrollArea.setWidgetResizable(False)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 170, len(self.dataList)*30))
		self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		
		
		# self.radioButton = QtWidgets.QRadioButton(self.scrollAreaWidgetContents)
		# self.radioButton.setGeometry(QtCore.QRect(30, 20, 89, 16))
		# self.radioButton.setObjectName("radioButton")

		for nameNum in range(len(self.dataList)):
			n = setattr(self, "cb%d" % nameNum, QCheckBox('%s' % (self.dataList[nameNum]), self.scrollAreaWidgetContents))
			m = getattr(self, "cb%d" % nameNum)
			m.move(10, textpostion(nameNum)-50)
		
		
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.bt = QtWidgets.QPushButton(self)
		self.bt.setGeometry(QtCore.QRect(70, 270, 75, 23))
		self.bt.setObjectName("pushButton_2")

		self.setWindowTitle("Form")
		# self.radioButton.setText("RadioButton")
		# self.pushButton.setText("PushButton")
		self.bt.setText("确定")
		self.bt.clicked.connect(self.btnpress)
		#bt.clicked.connect(self.close)
		#self.resize(200,500)
		self.show()

	def btnpress(self):
		L_check = []
		for pipe in range(len(self.dataList)):
			m = getattr(self, "cb%d" % pipe)
			if m.isChecked():
				# print("pipe"),
				L_check.append(self.dataList[pipe])
		self.mySignal.emit(L_check)
		# self.dataList=dbNameSearch()	
		# l = self.dataList
		# sum = 0
		# for nameNum in range(len(self.dataList)):
			# n = setattr(self, "cb%d" % nameNum, QRadioButton('%s' % (self.dataList[nameNum]), self))
			# m = getattr(self, "cb%d" % nameNum)
			# m.move(30, textpostion(nameNum))
			# sum = max(sum, textpostion(nameNum))
		# # button.setFixedSize(QtCore.QSize(60,30))
		# # m=getattr(self,"cb%d"%pipe)
		# # self.cb1 = QCheckBox('%s'%(l[0]),self)
		# # self.cb2 = QCheckBox('%s'%(l[1]),self)
		# # self.cb3 = QCheckBox('我的',self)
		# # self.cb4 = QCheckBox('宝贝',self)

		# #w.setLayout(self.vbox)
		# self.bt = QPushButton('提交', self)

		# #self.resize(300, sum + 100)
		# self.setWindowTitle('选择dbName')

		# # self.cb2.move(30,50)
		# # self.cb3.move(30,80)
		# # self.cb4.move(30,110)

		# self.bt.move(20, sum + 50)

		# #self.qxbtn.stateChanged.connect(self.changecb1)
		# # self.cb2.stateChanged.connect(self.changecb2)
		# # self.cb3.stateChanged.connect(self.changecb2)
		# # self.cb4.stateChanged.connect(self.changecb2)
		# self.bt.clicked.connect(self.btnpress)
		# #bt.clicked.connect(self.close)
		# self.resize(200,500)
		# self.show()

	# def btnpress(self):
		# L_check = []
		# for pipe in range(len(self.dataList)):
			# m = getattr(self, "cb%d" % pipe)
			# if m.isChecked():
				# # print("pipe"),
				# L_check.append(self.dataList[pipe])
		# self.mySignal.emit(L_check)
	


		

if __name__ == "__main__":
	app = 0
	app = QApplication(sys.argv)
	app.setWindowIcon(QIcon(":/icon.png"))
	app.setOrganizationName("Qtrac Ltd.")
	app.setOrganizationDomain("qtrac.eu")
	app.setApplicationName("Tabbed Text Editor")
	form = MainWindow()
	form.show()
	sys.exit(app.exec_())




