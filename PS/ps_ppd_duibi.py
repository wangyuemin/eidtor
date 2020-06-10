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
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='work770')
cursor = conn.cursor()
def search_sql(colName,JPN_contxt):
	quarySql="SELECT %s FROM ppd where JPN='%s'"%(colName,JPN_contxt)
	cursor.execute(quarySql) 
	conn.commit() 
	urlData = cursor.fetchall()
	content=urlData[0][0]
	return(content)
def lineList(text_name,file):
	htmlf=open(text_name,mode='r',encoding='%s'%(L_dict[file]),errors='ignore')
	htmlcont=htmlf.read()
		
	lineList=htmlcont.split('\n')
	return(lineList)
def PPD_bidui(file,path,txtname,path_make,txtname_make,file1):
	#RC_path=r'C:\Users\Xuexiaobo\Desktop\各机型db\756\PJF_PX756Enh2\Source\CHS'
	
	text_name=r'%s\%s\%s'%(path,file,txtname)
	text_name_make=r'%s\%s\%s'%(path_make,file,txtname_make)
	text_name_CHS=r'%s\%s\%s'%(path,file1,txtname)
	lineList_orgin=lineList(text_name,file)
	lineList_make=lineList(text_name_make,file)
	lineList_CHS=lineList(text_name_CHS,file1)
	#print(lineList_orgin,lineList_make)
	lineList_orgin_num=len(lineList_orgin)
	l=lineList_orgin.copy()
	l_CHS=lineList_CHS.copy()
	remove_list=[]
	for num_remove in range(lineList_orgin_num):
		# print(lineList_orgin_num)
		# print(len(lineList_orgin))
		# print(len(l))
		# print(num_remove)
		if lineList_orgin[num_remove] not in lineList_make:
			#l.remove(lineList_orgin[num_remove])
			remove_list.append(num_remove)
		elif lineList_make.count(lineList_orgin[num_remove])>1:
			#l.remove(lineList_orgin[num_remove])
			remove_list.append(num_remove)
		elif lineList_orgin.count(lineList_orgin[num_remove])>1:
			#l.remove(lineList_orgin[num_remove])
			remove_list.append(num_remove)
	for num in remove_list:
		l.remove(lineList_orgin[num])
		l_CHS.remove(lineList_CHS[num])
		# else:
			# pass
	for num in range(len(lineList_make)):
		line_txt=lineList_make[num]
		if lineList_make[num] not in l:
			
			l.insert(num,'abczxy%s'%lineList_make[num])
			if '光沢モード' in lineList_make[num]:
				colName=file1
				JPN_contxt='光沢モード'
				CHS_context=search_sql(colName,JPN_contxt)
				line_txt=line_txt.replace('光沢モード',CHS_context)
			elif 'プリンター設定' in lineList_make[num]:
				colName=file1
				JPN_contxt='プリンター設定'
				CHS_context=search_sql(colName,JPN_contxt)
				line_txt=line_txt.replace('プリンター設定',CHS_context)
			elif 'なし' in lineList_make[num]:
				colName=file1
				JPN_contxt='なし'
				CHS_context=search_sql(colName,JPN_contxt)
				line_txt=line_txt.replace('なし',CHS_context)				
			elif 'あり' in lineList_make[num]:
				colName=file1
				JPN_contxt='あり'
				CHS_context=search_sql(colName,JPN_contxt)
				line_txt=line_txt.replace('あり',CHS_context)		
			l_CHS.insert(num,'abczxy%s'%line_txt)
	# # for num in range(len(lineList_make)):
		# # if lineList_make[num] not in l:
			# # l.insert(num,lineList_make[num])
	s='\n'.join(l_CHS)
	s=s.replace('abczxy','')
	fp=open(r'%s\%s\%s'%(path_make,file1,txtname_make),mode='w',encoding='%s'%(L_dict[file1]),errors='ignore')
	fp.write(s)
	fp.close()
	# try:
		# htmlf=open(text_name,mode='r',encoding='utf-16')
		# htmlcont=htmlf.read()
		# #print(htmlcont)
	# except:


path_make=r'I:\PX_770\sinps\PX770'
path=r'I:\PX_770\sinps\PX756Enh2\PX756C8Enh2'
#fileList=['ENU','JPN','CHS','CHT','DEU','ESP','FRA','ITA','KOR','PTB']
file='JPN'
#file1='CHS'
txtname='OKC844W3.PPD'
txtname_make='OK5450W3.PPD'
#file_list=['CHS','CHT','DEU','ESP','FRA','ITA','KOR','PTB']
file_list=['CHS']
for file1 in file_list:
	PPD_bidui(file,path,txtname,path_make,txtname_make,file1)

			