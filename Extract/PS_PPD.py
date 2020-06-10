from openpyxl import Workbook
from openpyxl import load_workbook
import pymysql
import xlrd
import xlwt
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from openpyxl.styles import Font
from openpyxl.styles.colors import RED
from collections import Counter
import os
import sqlite3
import subprocess
L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}

def createHhc(host,port,tableName,dbName):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	#sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"

	sql="CREATE TABLE `%s` (`id` INT NOT NULL AUTO_INCREMENT ,`url` TEXT NULL,`title` TEXT NULL,`tab` TEXT NULL,`Control_id` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"%(tableName)
	#print(sql)

	cursor.execute(sql)
	conn.commit()
# def createHhk():
	# conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='753')
	# cursor = conn.cursor()
	# #sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	# #sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	# sql = "CREATE TABLE `hhk` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	# print(sql)
	# #print(sql)
	# cursor.execute(sql) 
	# conn.commit()
def addColumn(host,port,table,lanuage,dbName):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql="ALTER TABLE `%s`ADD COLUMN `%s` TEXT NULL;"%(table,lanuage)
	cursor.execute(sql) 
	conn.commit()
#createTable()
def creattable(host,port,dbName,path):
	tableList=['ppd']
	for tableName in tableList:
		createHhc(host,port,tableName,dbName)
		namesFile=os.listdir(path)
		namesList=[]
		for file in namesFile:
			if file in ['CAT','CHS','CHT','CSY','DAN','DEU','ELL','ENU','ESP','FIN','FRA','HUN','ITA','JPN','KOR','NLD','NOR','PLK','PTB','PTG','RUS','SVE','TRK']:
				namesList.append(file)
		for file in namesList:

			addColumn(host,port,tableName,file,dbName)


def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	print(value)
	try:
		sql = 'INSERT INTO ppd (url,title,%s) VALUES("%s","%s","%s")'%value
		print(sql)
		cursor.execute(sql) 
		conn.commit()
	except:
		sql = "INSERT INTO ppd (url,title,%s) VALUES('%s','%s','%s')"%value
		print(sql)
		cursor.execute(sql) 
		conn.commit()	
def upData(cursor,value):
	try:
		sql1='UPDATE ppd SET %s="%s" WHERE title="%s" and url="%s"'%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1="UPDATE ppd SET %s='%s' WHERE title='%s' and url='%s'"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def PS_PPD(dbName,file,path,cursor):
	#RC_path=r'C:\Users\Xuexiaobo\Desktop\各机型db\756\PJF_PX756Enh2\Source\CHS'

	indexFile=os.listdir('%s\%s'%(path,file))
	for txtname in indexFile:
		#if os.path.splitext(txtname)[-1] == ".PPD":
		text_name=r'%s\%s\%s'%(path,file,txtname)
		print(text_name)
		ControlId_list=[]
		
		# try:
			# htmlf=open(text_name,mode='r',encoding='utf-16')
			# htmlcont=htmlf.read()
			# #print(htmlcont)
		# except:
		htmlf=open(text_name,mode='r',encoding='%s'%(L_dict[file]),errors='ignore')
		htmlcont=htmlf.read()
			
		line=htmlcont.split('\n')
		num=0
		begin_num=9999999
		end_num=0
		for j in range(len(line)):
			i=line[j]
			num=num+1
			if '*OpenUI' in i:
				#print(1111)
				begin_num=num
			if i=='CloseUI:':
				end_num=num
			if end_num>begin_num:
				begin_num=9999999
			# else:
				# print(777)
				# print(i)
			if (begin_num<=num):
				# print(6666)
				if '"' in i:
					if '"' in i and '/' in i and ':' in i:
						title=i.split('/')[0].split('*')[1].strip()
						context=i.split('/')[1].split(':')[0].strip()
					try:

						quarySql='SELECT * FROM ppd WHERE url="%s" and title="%s"'%(txtname,title.replace("'","''").strip())
						print(quarySql)

						cursor.execute(quarySql) 

						conn.commit()
					except:
						quarySql="SELECT * FROM ppd WHERE url='%s' and title='%s'"%(txtname,title.replace("'","''").strip())
						print(quarySql)

						cursor.execute(quarySql) 

						conn.commit()	
					urlData = cursor.fetchall()
					print(urlData)
					if urlData==():
						print(urlData)
						storeData(cursor,(file,txtname,title,context))
					else:
						upData(cursor,(file,context.strip(),title,txtname))
					print(title)
					print(context)
					# i=i.strip()
					# title=i.split('"')[0]
					# id=i.split('",')[1].strip().split(',')[0]
					# context=i.split('"')[1]
					# ControlId_list.append(id)
				else:
					if '*OpenUI' in i and ':' in i and '/' in i:
						print(i)
						title=i.split('/')[0].split('*')[2].strip()
						context=i.split('/')[1].split(':')[0].strip()
						try:

							quarySql='SELECT * FROM ppd WHERE url="%s" and title="%s"'%(txtname,title.replace("'","''").strip())
							print(quarySql)

							cursor.execute(quarySql) 

							conn.commit()
						except:
							quarySql="SELECT * FROM ppd WHERE url='%s' and title='%s'"%(txtname,title.replace("'","''").strip())
							print(quarySql)

							cursor.execute(quarySql) 

							conn.commit()	
						urlData = cursor.fetchall()
						print(urlData)
						if urlData==():
							print(urlData)
							storeData(cursor,(file,txtname,title,context))
						else:
							upData(cursor,(file,context.strip(),title,txtname))
					else:
						pass
			if '*OpenGroup:' in i:
				title=i.split('/')[0].split('*')[1].strip()
				context=i.split('/')[1].strip()	
				try:

					quarySql='SELECT * FROM ppd WHERE url="%s" and title="%s"'%(txtname,title.replace("'","''").strip())
					print(quarySql)

					cursor.execute(quarySql) 

					conn.commit()
				except:
					quarySql="SELECT * FROM ppd WHERE url='%s' and title='%s'"%(txtname,title.replace("'","''").strip())
					print(quarySql)

					cursor.execute(quarySql) 

					conn.commit()	
				urlData = cursor.fetchall()
				print(urlData)
				if urlData==():
					print(urlData)
					storeData(cursor,(file,txtname,title,context))
				else:
					upData(cursor,(file,context.strip(),title,txtname))
				
#path=r'E:\PX_770\sinps\xX760\xX760'
def PPD(host,port,dbName,path):
#path=r'E:\PX_770\sinps\PX756Enh2\PX756C8Enh2'
	namesFile=os.listdir(path)
	fileList=[]
	for file in namesFile:
		if file in ['CAT','CHS','CHT','CSY','DAN','DEU','ELL','ENU','ESP','FIN','FRA','HUN','ITA','JPN','KOR','NLD','NOR','PLK','PTB','PTG','RUS','SVE','TRK']:
			fileList.append(file)
	#fileList=['ENU','JPN','CHS','CHT','DEU','ESP','FRA','ITA','KOR','PTB']
	#txtName='OKC844W3.PPD'
	conn1 = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor1 = conn1.cursor()
	
	createsql='CREATE DATABASE %s'%(dbName)
	try:
		cursor1.execute(createsql)
		conn1.commit()
	except:
		pass
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	cursor.execute("drop table if exists ppd")
	creattable(host,port,dbName,path)
	for file in fileList:
		PS_PPD(dbName,file,path,cursor)
	lanName=','.join(fileList)
	sql='create TABLE ppddis select distinct %s FROM ppd'%(lanName)
	cursor.execute(sql)
	sql1='drop table if exists ppd'
	sql2='RENAME TABLE ppddis TO ppd'
	sql3="ALTER TABLE ppd ADD id INT(4) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;"
	cursor.execute(sql1)
	cursor.execute(sql2)
	cursor.execute(sql3)
	conn1.commit()
			