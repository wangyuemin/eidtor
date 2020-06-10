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
#path_dialog_xml_font = r'.\PJF_PX753\Localize'
def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree
def storeData(cursor,value):
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	sql = 'INSERT INTO dialog_xml_font (url,%s) VALUES("%s","%s")'%value
	#print(sql)
	#print(sql)
	cursor.execute(sql) 
	conn.commit() 
def upData(cursor,value):
	try:
		sql1="UPDATE dialog_xml_font SET %s='%s' WHERE url='%s'"%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE dialog_xml_font SET %s="%s" WHERE url="%s"'%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
def dialog_xml_font_text(file_name):
	# files_names=r'C:\Users\Xuexiaobo\python_code\Help\%s\HELP'%(language)
	# LangeEncoding=L_dict['%s'%(language)]
	# names=os.listdir(files_names)
	# for i in range(len(names)):
	dialog_xml_fontlf=open('%s\%s'%(files_names,file_name),mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
	dialog_xml_fontlcont=dialog_xml_fontlf.read()
	#print(dialog_xml_fontlcont)
	soup= BeautifulSoup(dialog_xml_fontlcont,'html.parser')
	h_soup=soup.dialog_xml_fontl
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
def insert(fileName,lanName,cursor,files_names,namesFile1):
	text_name='%s\%s'%(files_names,fileName)
	dom = xml.dom.minidom.parse(text_name)
	tree = read_xml(text_name)
	root = dom.documentElement
	textName=fileName

	FontAttrib=tree.findall("Font")[0].attrib
	
	if lanName==namesFile1[0]:
		storeData(cursor,(lanName,fileName,FontAttrib))
	else:
		upData(cursor,(lanName,FontAttrib,fileName))
#urlData = cursor.fetchall()
def dialog_xml_font(host,port,dbName,path_dialog_xml_font):
	colList=['JPN','ENU','CHS','CHT','CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	namesFile1=os.listdir(path_dialog_xml_font) #CHT
	namesFile=[]
	for file in namesFile1:
		if file!='Common':
			namesFile.append(file)
	for lanName in namesFile:
		row_num=0
		files_names=r'%s\%s\Dialog'%(path_dialog_xml_font,lanName)
		#print(namesFile[txt_num])
		LangeEncoding=L_dict['%s'%(lanName)]
		names=os.listdir(files_names)
		LTask=[]
		for i in names:
			insert(i,lanName,cursor,files_names,namesFile)
			# LTask.append(g)
		# for j in LTask:
			# j.join()


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			