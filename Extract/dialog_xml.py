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
import pymysql
import os,sys
from bs4 import BeautifulSoup
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from xml.etree.ElementTree import ElementTree,Element
#path_dialog_xml = r'.\PJF_PX753\Localize'
def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree
def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	sql = 'INSERT INTO dialog_xml (url,title,Control_id,%s) VALUES("%s","%s","%s","%s")'%value
	print(sql)
	#print(sql)
	cursor.execute(sql) 
	conn.commit() 
def upData(cursor,value):
	try:
		sql1="UPDATE dialog_xml SET %s='%s' WHERE url='%s' and title='%s' and Control_id='%s'"%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE dialog_xml SET %s="%s" WHERE url="%s" and title="%s" and Control_id="%s"'%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def storeData_P(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	sql = 'INSERT INTO dialog_xml (url,title,Control_id,%s,%s,%s,%s) VALUES("%s","%s","%s","%s","%s","%s","%s")'%value
	#print(sql)
	#print(sql)
	cursor.execute(sql) 
	conn.commit()
def upData_P(cursor,value):
	try:
		sql1="UPDATE dialog_xml SET %s='%s',%s='%s',%s='%s',%s='%s' WHERE url='%s' and title='%s' and Control_id='%s'"%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE dialog_xml SET %s="%s",%s="%s",%s="%s",%s="%s" WHERE url="%s" and title="%s" and Control_id="%s"'%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def dialog_xml_text(file_name):
	# files_names=r'C:\Users\Xuexiaobo\python_code\Help\%s\HELP'%(language)
	# LangeEncoding=L_dict['%s'%(language)]
	# names=os.listdir(files_names)
	# for i in range(len(names)):
	dialog_xmllf=open('%s\%s'%(files_names,file_name),mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
	dialog_xmllcont=dialog_xmllf.read()
	#print(dialog_xmllcont)
	soup= BeautifulSoup(dialog_xmllcont,'html.parser')
	h_soup=soup.dialog_xmll
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
			#print(i)
			textList.append(i)
	for ji in textList[2:]:
		str1=str1+ji+''
	return (str1)

#urlData = cursor.fetchall()
def insert(fileName,lanName,cursor,files_names,namesFile1):
	print(lanName)
	print(namesFile1)
	text_name='%s\%s'%(files_names,fileName)
	tree = read_xml(text_name)
	dom = xml.dom.minidom.parse(text_name)
	root = dom.documentElement
	textName=fileName
	#print(textName)
	P_style='%s_style'%(lanName)
	P_exstyle='%s_exstyle'%(lanName)
	P_class='%s_class'%(lanName)
	tagControl = root.getElementsByTagName('Control')
	num1=0
	tagCaption = root.getElementsByTagName('Caption')
	styletext=tree.findall("Style")[0].text
	#try:
	for indexCaption in tagCaption:
		pfCaption=indexCaption.firstChild.data
		#print(pfCaption)				#标题
		if lanName==namesFile1[0]:
			storeData(cursor,(lanName,fileName,'Caption','Caption',pfCaption))
		else:
			upData(cursor,(lanName,pfCaption,fileName,'Caption','Caption'))
	# except:
		# pass
	#print(len(tagCaption))
	#try:
	FontAttrib=tree.findall("Font")[0].attrib
	tagFont = root.getElementsByTagName('Font')
	for indexFont in tagFont:
		pfFont=indexFont.firstChild.data
		#print(pfFont)				#字体
		if lanName==namesFile1[0]:
			storeData(cursor,(lanName,fileName,'Font',FontAttrib,pfFont))
		else:
			upData(cursor,(lanName,pfFont,fileName,'Font',FontAttrib))
		#print(len(tagFont))
	# except:
		# pass
	#try:
	if lanName==namesFile1[0]:
		storeData(cursor,(lanName,fileName,'style','style',styletext))
	else:
		upData(cursor,(lanName,styletext,fileName,'style','style'))
	# except:
		# pass
	list_id=[]
	for b in tagControl:
		#print (b.nodeName)
		pd=b.getAttribute("id")
		list_id.append(pd)					#control_id
		num1+=1
	per=ET.parse(text_name)
	p=per.findall('Controls')
	#print(p)
	#print(len(tagControl))
	for k in range(num1):
		node=list(p[0])[k]
		root = dom.documentElement
		pd=list_id[k]
		#print(list(node)[0].text)
		pf=list(node)[0].text
		#print(pf)						#文本
		pstyle=list(node)[1].text
		#print(pstyle)	#style	
		pExStyle=list(node)[2].text
		#print(pExStyle)	#ExStyle
		pClass=list(node)[3].text
		#print(pClass)	#Class
		if lanName==namesFile1[0]:
			storeData_P(cursor,(lanName,P_style,P_exstyle,P_class,fileName,'Control',pd,pf,pstyle,pExStyle,pClass))
		else:
			upData_P(cursor,(lanName,pf,P_style,pstyle,P_exstyle,pExStyle,P_class,pClass,fileName,'Control',pd))
def dialog_xml(host,port,dbName,path_dialog_xml):
	print('dialog')
	colList=['JPN','ENU','CHS','CHT','CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	namesFile1=os.listdir(path_dialog_xml) #CHT
	namesFile=[]
	for file in namesFile1:
		if file!='Common':
			namesFile.append(file)
	for lanName in namesFile:
		print(lanName)
		row_num=0
		files_names=r'%s\%s\Dialog'%(path_dialog_xml,lanName)
		#print(lanName)
		LangeEncoding=L_dict['%s'%(lanName)]
		names=os.listdir(files_names)
		gol_number=1
		LTask=[]
		for i in names:
			insert(i,lanName,cursor,files_names,namesFile)
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			