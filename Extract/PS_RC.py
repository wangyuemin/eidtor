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
import codecs
L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
Ldict={'j':'JPN','e':'ENU','bp':'PTB','chs':'CHS','cht':'CHT','de':'DEU','es':'ESP','fr':'FRA','it':'ITA','kor':'KOR'}
def createHhc(host,port,tableName,dbName):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	#sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	cursor.execute("drop table if exists %s"%(tableName))
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

def creattable(host,port,namesList,dbName,path):
	tableList=['rc']
	for tableName in tableList:
		createHhc(host,port,tableName,dbName)
		namesFile=os.listdir(path)
		namesListL=[]
		for file in namesFile:
			if file.split('.')[0] in namesList:
				namesListL.append(file.split('.')[0])
		for file in namesListL:

			addColumn(host,port,tableName,file,dbName)
def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	try:
		sql = 'INSERT INTO rc (title,%s,tab) VALUES("%s","%s","%s")'%value
		print(sql)
		cursor.execute(sql) 
		conn.commit()
	except:
		sql = "INSERT INTO rc (title,%s,tab) VALUES('%s','%s','%s')"%value
		print(sql)
		cursor.execute(sql) 
		conn.commit()	
def upData(cursor,value):
	try:
		sql1='UPDATE rc SET %s="%s" WHERE title="%s" and tab="%s"'%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1="UPDATE rc SET %s='%s' WHERE title='%s' and tab='%s'"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def PS_RC(namesList,file,path,dbName):
	#RC_path=r'C:\Users\Xuexiaobo\Desktop\各机型db\756\PJF_PX756Enh2\Source\CHS'
	text_name=r'%s\%s.rc'%(path,file)
	print(file)
	enCoding=L_dict[Ldict[file.split('_')[-1]]]
	print(enCoding)
	ControlId_list=[]
	try:
		htmlf=open(text_name,mode='r',encoding='utf-16',errors='ignore')
		htmlcont=htmlf.read()
		#print(htmlcont)
		print(1)
	except:
		try:
			htmlf=open(text_name,mode='r',encoding='utf-8')
			htmlcont=htmlf.read()
			print(2)
		except:
			htmlf=open(text_name,mode='r',encoding=enCoding,errors='ignore')
			htmlcont=htmlf.read()
			print(3)
	print(htmlcont)
	line=htmlcont.split('\n')
	num=0
	begin_num=9999999
	end_num=0
	for j in range(len(line)):
		i=line[j]
		#print(i)
		num=num+1
		if 'CAPTION' in i:
			#print(1111)
			begin_num=num
		if i=='END':
			end_num=num
		if end_num>begin_num:
			begin_num=9999999
		# else:
			# print(777)
			# print(i)
		if (begin_num<=num):
			# print(6666)
			if '"' in i:
				if 'CAPTION' in i:
					global tab_name
					if 'DIALOG DISCARDABLE' in line[num-3] or 'DIALOGEX' in line[num-3]:
						tab_name=line[num-3].split(' ')[0]
						#title='CAPTION_%s'%(tab_name)
						title='CAPTION'
						context=i.split('"')[1].split('"')[0]
					else:
						tab_name=line[num-4].split(' ')[0]
						#title='CAPTION_%s'%(tab_name)
						title='CAPTION'
						context=i.split('"')[1].split('"')[0]
				elif 'FONT' in i and '_' not in i:
					if 'DIALOG DISCARDABLE' in line[num-4] or 'DIALOGEX' in line[num-4]:
						tab_name=line[num-4].split(' ')[0]
						#title='FONT_%s'%(tab_name)
						title='FONT'
						context=i.split('"')[1].split('"')[0]
					else:
						tab_name=line[num-5].split(' ')[0]
						#title='FONT_%s'%(tab_name)
						title='FONT'
						context=i.split('"')[1].split('"')[0]
				else:
					try:
						if i.split(',')[1].split(',')[0]=='-1':
							pass
						else:
							if i.split('",')[1]=='':
								title=line[num].split(',')[0]
								context=i.split('"')[1].split('"')[0]
								print(i)
								print(title)
								print(context)
								#print(title,context)
							else: 
								if i.count('"')==2 and 'Button' in i:								
									pass
								else:
									title=i.split('",')[1].split(',')[0]
									context=i.split('"')[1].split('"')[0]
					except:
						pass
			elif 'IDC_' in i and ',' in i and '"' not in i:
				context=''
				title='IDC'+i.split(',')[0].split('IDC')[1]
				#print(i)
				#print(title)
			else:
				pass
			try:
				try:
					#title=title.replace("'","''").strip()
					quarySql='SELECT * FROM rc WHERE title="%s" and tab="%s"'%(title,tab_name)
					#print(quarySql)

					cursor.execute(quarySql) 

					conn.commit()
				except:
					#title=title.replace("'","''").strip()
					quarySql="SELECT * FROM rc WHERE title='%s' and tab='%s'"%(title,tab_name)
					#print(quarySql)

					cursor.execute(quarySql) 

					conn.commit()
					
				urlData = cursor.fetchall()
				#print(urlData)
				if urlData==():
					if '|' in title:
						pass
					else:
						#title=title.replace("'","''").strip()
						print(context)
						context=context.replace('\\n','\\\\n').replace('\\r','\\\\r').replace('\\t','\\\\t').replace("\\'","\\\\\\'")
						print(context)
						storeData(cursor,(file,title,context,tab_name))
				else:
					print(context)
					context=context.replace('\\n','\\\\n').replace('\\r','\\\\r').replace('\\t','\\\\t').replace("\\'","\\\\\\'")
					print(context)
					#title=title.replace("'","''").strip()

					quarySql="SELECT %s FROM rc WHERE title='%s' and tab='%s'"%(file,title,tab_name)
					#print(quarySql)
					cursor.execute(quarySql) 
					conn.commit()
					urlData = cursor.fetchall()
					print(urlData)
					if urlData[0][0]==None:					
						upData(cursor,(file,context,title,tab_name))
			except:
				pass
				#print(title)
				#print(context)
				# i=i.strip()
				# title=i.split('"')[0]
				# id=i.split('",')[1].strip().split(',')[0]
				# context=i.split('"')[1]
				# ControlId_list.append(id)

	for i in line:
		num=num+1
		if 'STRINGTABLE DISCARDABLE' in i:
			#print(1111)
			begin_num=num
		if i=='END':
			end_num=num
		if end_num>begin_num:
			begin_num=9999999
		# else:
			# print(777)
			# print(i)
		if (begin_num<num):
			# print(6666)
			if '"' in i:
				tab_name='STRINGTABLE DISCARDABLE'
				title=i.split('"')[0].strip()
				context=i.split('"')[1].split('"')[0]
				# title=i.split('"')[0]
				# id=i.split('",')[1].strip().split(',')[0]
				# context=i.split('"')[1]
				# ControlId_list.append(id)
				quarySql='SELECT * FROM rc WHERE title="%s" and tab="%s"'%(title.replace("'","''").strip(),tab_name)
				cursor.execute(quarySql) 
				conn.commit() 
				urlData = cursor.fetchall()
				if urlData==():
					#title=title.replace("'","''").strip()
					print(context)
					context=context.replace('\\n','\\\\n').replace('\\r','\\\\r').replace('\\t','\\\\t').replace("\\'","\\\\\\'")
					print(context)
					storeData(cursor,(file,title,context,tab_name))
				else:
					print(context)
					context=context.replace('\\n','\\\\n').replace('\\r','\\\\r').replace('\\t','\\\\t').replace("\\'","\\\\\\'")
					print(context)
					#title=title.replace("'","''").strip()
					upData(cursor,(file,context,title,tab_name))
				#print(title)
				#print(context)
			else:
				pass
def RC(host,port,dbName,path):
	conn1 = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor1 = conn1.cursor()
	
	createsql='CREATE DATABASE %s'%(dbName)
	try:
		cursor1.execute(createsql)
		conn1.commit()
	except:
		pass
	global conn
	global cursor
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#path=r'C:\Users\Xuexiaobo\Desktop\readPS\rc_jp'
	#dbName='ps'
	namesFile=os.listdir(path)
	namesList=[]
	for file in namesFile:
		if os.path.splitext(file)[-1] == ".rc":
			namesList.append(os.path.splitext(file)[0])
		else:
			pass
	cursor.execute("drop table if exists rc")
	creattable(host,port,namesList,dbName,path)
	print(namesList)
	for file in namesList:
		print(file)
		PS_RC(namesList,file,path,dbName)


