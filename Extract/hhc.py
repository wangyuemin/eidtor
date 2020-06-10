import pymysql
import os,sys
from bs4 import BeautifulSoup
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
import pymysql
import os
from gevent import monkey; monkey.patch_all()
import gevent
import time
from xml.etree.ElementTree import ElementTree,Element
import xml.dom.minidom
from xml.etree import ElementTree as ET
import pymysql
import os,sys
from bs4 import BeautifulSoup
#path_hhk = r'.\PJF_PX753\Localize\Common\RBK\DP_Generated\HELP'
def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	try:
		sql = 'INSERT INTO hhc (url,%s) VALUES("%s","%s")'%value
		print(sql)
		#print(sql)
		cursor.execute(sql) 
		conn.commit() 
	except:
		sql1="INSERT INTO hhc (url,%s) VALUES('%s','%s')"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()		
def upData(cursor,value):
	try:
		sql1="UPDATE hhc SET %s='%s' WHERE url='%s'"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE hhc SET %s="%s" WHERE url="%s"'%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def upDataID(cursor,value):
	try:
		sql1="UPDATE hhc SET %s='%s' WHERE id='%s'"%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE hhc SET %s="%s" WHERE id="%s"'%value
		print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def hhk_text(file_name):
	# files_names=r'C:\Users\Xuexiaobo\python_code\Help\%s\HELP'%(language)
	# LangeEncoding=L_dict['%s'%(language)]
	# names=os.listdir(files_names)
	# for i in range(len(names)):
	hhklf=open('%s\%s'%(files_names,file_name),mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
	hhklcont=hhklf.read()
	#print(hhklcont)
	soup= BeautifulSoup(hhklcont,'html.parser')
	h_soup=soup.hhkl
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

def insert(lanName,path_hhk,cursor,L_dict):
	print(lanName)
	files_names=r'%s\%s'%(path_hhk,lanName)
	LangeEncoding=L_dict['%s'%(lanName)]
	names=[]
	for ty_name in os.listdir(files_names):
		if (os.path.splitext(ty_name)[-1] == ".hhc"):
			names.append(ty_name)     #HELP_1200.hhc
		else:
			pass
	for i in range(len(names)):
		hcc_name=names[i]
		text_name='%s\%s'%(files_names,names[i])
		htmlf=open(text_name,mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
		htmlcont=htmlf.read()
		#print(htmlcont)
		soup= BeautifulSoup(htmlcont,'html.parser')
		h_s=soup.find_all("param")
		s_value=[]
		for j in range(len(h_s)):
			#print(len(h_s))
			#print(j)
			#print(row_num)
			#print(i['name'])
			print(h_s[j]['value'])
			if (h_s[j]['value'] not in ["index","toc","0x800027","0x100"]):
				s_value.append(h_s[j]['value'])  #s_value 
		L_context=[]
		for k in range(len(s_value)):
			if (k%2):
				url_text=s_value[k]
				if '/' in url_text:
					#print(0)
					url_text=url_text.split('/')[-1]
				else:
					#print(1)
					url_text=url_text.split('\\')[-1]
				#print( url_text)
			else:
				context_text=s_value[k]
			if (k%2):
				quarySql='SELECT * FROM hhc WHERE url="%s"'%(url_text)
				print(quarySql)
				cursor.execute(quarySql) 
				conn.commit()
				urlData = cursor.fetchall()
				if urlData==():

					storeData(cursor,(lanName,url_text,context_text))
				else:
					idList=[item[0] for item in urlData]
					print(idList)
					num=0
					for id in idList:
						sql='SELECT %s FROM hhc WHERE id="%s"'%(lanName,id)
						cursor.execute(sql) 
						conn.commit()
						urlData = cursor.fetchall()
						print(urlData)
						if urlData[0][0]==None:
							num=1
							upDataID(cursor,(lanName,context_text,id))
							break
						# elif urlData[0][0]==context_text:
							# num=1
							# break
						else:
							pass
					if num==0:
						storeData(cursor,(lanName,url_text,context_text))
def hhc(host,port,dbName,path_hhc):
	colList=['JPN','ENU','CHS','CHT','CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	namesFile=os.listdir(path_hhc) #CHT
	LTask=[]
	for lanName in namesFile:
		insert(lanName,path_hhc,cursor,L_dict)
