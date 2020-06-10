import pymysql
import os,sys
from bs4 import BeautifulSoup
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from gevent import monkey; monkey.patch_all()
import gevent
import time
#path_stringdefinition = r'.\PJF_PX753\Localize'
def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	sql = 'INSERT INTO stringdefinition (url,%s) VALUES("%s","%s")'%value
	print(sql)
	#print(sql)
	cursor.execute(sql) 
	conn.commit() 
def upData(cursor,value):
	try:
		sql1="UPDATE stringdefinition SET %s='%s' WHERE url='%s'"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE stringdefinition SET %s="%s" WHERE url="%s"'%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def stringdefinition_text(file_name):
	# files_names=r'C:\Users\Xuexiaobo\python_code\Help\%s\HELP'%(language)
	# LangeEncoding=L_dict['%s'%(language)]
	# names=os.listdir(files_names)
	# for i in range(len(names)):
	stringdefinitionlf=open('%s\%s'%(files_names,file_name),mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
	stringdefinitionlcont=stringdefinitionlf.read()
	#print(stringdefinitionlcont)
	soup= BeautifulSoup(stringdefinitionlcont,'html.parser')
	h_soup=soup.stringdefinitionl
	list_descendants=[]		
	f = open(r"C:\Users\Xuexiaobo\1.txt",'w',encoding='utf-8') 
	f.write(soup.text) 
	f.close()
	data = open(r"C:\Users\Xuexiaobo\1.txt",encoding='utf-8').read()
	listData=data.split('\n')
	textList=[]
	str1=''
	for i in listData:
		if i=='' or i=='\u3000':
			pass
		else:
			print(i)
			textList.append(i)
	for ji in textList[2:]:
		str1=str1+ji+''
	return (str1)
def insert(bbCont,lanName,cursor):
	pd=bbCont.getAttribute("id")
	quarySql="SELECT * FROM stringdefinition WHERE url='%s'"%(pd)
	print(quarySql)
	cursor.execute(quarySql) 
	conn.commit() 
	urlData = cursor.fetchall()
	print(pd)
	if urlData==():
		try:
			pf=bbCont.firstChild.data
			print(pf)
		except:
			pf='FFalse_wrong'
			print('false')
		storeData(cursor,(lanName,pd,pf))
	else:
		try:
			pf=bbCont.firstChild.data
			print(pf)
		except:
			pf='FFalse_wrong'
			print('false')
		upData(cursor,(lanName,pf,pd))
#urlData = cursor.fetchall()
def stringdefinition(host,port,dbName,path_stringdefinition):
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	colList=['JPN','ENU','CHS','CHT','CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	namesFile1=os.listdir(path_stringdefinition) #CHT
	namesFile=[]
	for file in namesFile1:
		if file!='Common':
			namesFile.append(file)
	for txt_num in range(len(namesFile)):
		row_num=0
		StringDefinition_names=r'%s\%s\StringDefinition.xml'%(path_stringdefinition,namesFile[txt_num])
		LangeEncoding=L_dict['%s'%(namesFile[txt_num])]
		dom = xml.dom.minidom.parse(StringDefinition_names)
		root = dom.documentElement
		bb = root.getElementsByTagName('String')
		listPd=[]
		LTask=[]
		for col in range(len(bb)):
			#print(bb[col])
			listPd.append(bb[col])
		for i in listPd:
			insert(i,namesFile[txt_num],cursor)
		#gevent.joinall(LTask)
		# for j in LTask:
			# j.join()
	
	
	
	
	
	
'''	
	for i in range(len(names)):
		text_name='%s\%s'%(files_names,names[i])
		dom = xml.dom.minidom.parse(text_name)
		root = dom.documentElement
		textName=names[i]
		tagControl = root.getElementsByTagName('Control')
		num1=0
		tagCaption = root.getElementsByTagName('Caption')
		try:
			for indexCaption in tagCaption:
				pfCaption=indexCaption.firstChild.data
				#print(pfCaption)				#标题
				if namesFile[txt_num]=='CHS':
					storeData((namesFile[txt_num],names[i],'Caption',i,pfCaption))
				else:
					upData((namesFile[txt_num],pfCaption,names[i],'Caption',i))
		except:
			pass
		#print(len(tagCaption))
		try:
			tagFont = root.getElementsByTagName('Font')
			for indexFont in tagFont:
				pfFont=indexFont.firstChild.data
				#print(pfFont)				#字体
				if namesFile[txt_num]=='CHS':
					storeData((namesFile[txt_num],names[i],'Font',i,pfFont))
				else:
					upData((namesFile[txt_num],pfFont,names[i],'Font',i))
			print(len(tagFont))
		except:
			pass
		list_id=[]
		for b in tagControl:
			#print (b.nodeName)
			pd=b.getAttribute("id")
			list_id.append(pd)					#control_id
			num1+=1
		per=ET.parse(text_name)
		p=per.findall('Controls')
		#print(p)
		num2=gol_number-num1
		#print(len(tagControl))
		for k in range(num1):
			node=list(p[0])[k]
			root = dom.documentElement
			pd=list_id[k]
			#print(list(node)[0].text)
			pf=list(node)[0].text
			print(pf)						#文本
			num2+=1
			if namesFile[txt_num]=='CHS':
				storeData((namesFile[txt_num],names[i],'Control',pd,pf))
			else:
				upData((namesFile[txt_num],pf,names[i],'Control',pd))
		#print(num1)

'''			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			