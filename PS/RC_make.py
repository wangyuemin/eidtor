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
def search_sql(colName,JPN_contxt):
	quarySql="SELECT %s FROM rc where JPN='%s'"%(colName,JPN_contxt)
	cursor.execute(quarySql) 
	conn.commit() 
	urlData = cursor.fetchall()
	content=urlData[0][0]
	return(content)
def PS_RC(lan,jpnName,dbName,path):
	#RC_path=r'C:\Users\Xuexiaobo\Desktop\各机型db\756\PJF_PX756Enh2\Source\CHS'
	text_name=r'%s'%(jpnName)
	ControlId_list=[]
	try:
		htmlf=open(text_name,mode='r',encoding='utf-16',errors='ignore')
		htmlcont=htmlf.read()
		#print(htmlcont)
	except:
		try:
			htmlf=open(text_name,mode='r',encoding='utf-8')
			htmlcont=htmlf.read()
		except:
			htmlf=open(text_name,mode='r',encoding='shift_jis',errors='ignore')
			htmlcont=htmlf.read()
	line=htmlcont.split('\n')
	lineNew=line
	num=0
	begin_num=9999999
	end_num=0
	for j in range(len(line)):
		i=line[j]
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
					if i.split(',')[1].split(',')[0]=='-1':
						pass
					else:
						if i.split('",')[1]=='':
							title=line[num].split(',')[0]
							context=i.split('"')[1].split('"')[0]
							print(title,context)
						else: 
							if i.count('"')==2 and 'Button' in i:								
								pass
							else:
								title=i.split('",')[1].split(',')[0]
								context=i.split('"')[1].split('"')[0]
			elif 'IDC_' in i and ',' in i and '"' not in i:
				context=''
				title='IDC'+i.split(',')[0].split('IDC')[1]
				#print(i)
				#print(title)
			else:
				pass
			try:
				lanContext=(search_sql(lan,context))
				i_new=i.replace(context,lanContext)
				lineNew.pop(j)
				lineNew.insert(j,i_new)
				#print(i)

			except:
				pass
			# try:
				# try:

					# quarySql='SELECT * FROM rc WHERE title="%s" and tab="%s"'%(title.replace("'","''").strip(),tab_name)
					# #print(quarySql)

					# cursor.execute(quarySql) 

					# conn.commit()
				# except:
					# quarySql="SELECT * FROM rc WHERE title='%s' and tab='%s'"%(title.replace("'","''").strip(),tab_name)
					# #print(quarySql)

					# cursor.execute(quarySql) 

					# conn.commit()
					
				# urlData = cursor.fetchall()
				# #print(urlData)
				# if urlData==():
					# if '|' in title:
						# pass
					# else:
						# storeData(cursor,(file,title.replace("'","''").strip(),context.replace("'","''"),tab_name))
				# else:
					# upData(cursor,(file,context.replace("'","''").strip(),title.replace("'","''").strip(),tab_name))
			# except:
				# pass
				#print(title)
				#print(context)
				# i=i.strip()
				# title=i.split('"')[0]
				# id=i.split('",')[1].strip().split(',')[0]
				# context=i.split('"')[1]
				# ControlId_list.append(id)

	for j in range(len(line)):
		i=line[j]
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
				#print(i)
				lanContext=(search_sql(lan,context))
				if lanContext !=None:
					i_new=i.replace(context,lanContext)
					#print(i_new)
					lineNew.pop(j)
					lineNew.insert(j,i_new)
				else:
					pass
					#print(i)
					#htmlf=htmlf.replace(i,i_new)
				# quarySql='SELECT * FROM rc WHERE title="%s" and tab="%s"'%(title.replace("'","''").strip(),tab_name)
				# cursor.execute(quarySql) 
				# conn.commit() 
				# urlData = cursor.fetchall()
				# if urlData==():
					# storeData(cursor,(file,title.replace("'","''").strip(),context.replace("'","''"),tab_name))
				# else:
					# upData(cursor,(file,context.replace("'","''"),title.replace("'","''").strip(),tab_name))
				# #print(title)
				# #print(context)
			# else:
				# pass
	s='\n'.join(lineNew)
	fp=open(r'%s\%s.rc'%(path,lan),mode='w',encoding='%s'%(L_dict[lan]),errors='ignore')
	fp.write(s)
	fp.close()
def RC(host,port,dbName,jpnName,lan,path):
	conn1 = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor1 = conn1.cursor()
	global conn
	global cursor
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#path=r'C:\Users\Xuexiaobo\Desktop\readPS\rc_jp'
	#dbName='ps'
	PS_RC(lan,jpnName,dbName,path)
		
dbName=r'rc1'
host='127.0.0.1'
port=3306
path=r'H:\Desktop\桌面7.15\各机型db\PS_Source\oemui\xX760_w2k'
jpnName=r'H:\Desktop\桌面7.15\各机型db\PS_Source\oemui\xX760_w2k\xX760_j.rc'
lanList=['CHS']
for lan in lanList:
	RC(host,port,dbName,jpnName,lan,path)


