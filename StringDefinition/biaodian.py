import pymysql
import os
import re
import html
# text_names=os.listdir(r'C:\Users\Xuexiaobo\Desktop\work\DP\PJF_PV702_Genric\Localize1\CHS\Dialog')
# colList=['RUS','CHS','CHT','CSY','DAN','ELL','FIN','HUN','NLD','NOR','PLK','KOR','PTB','PTG','SVE','TRK']
# for colName in colList:
	# for text_name in text_names:
		# type_name=r'C:\Users\Xuexiaobo\Desktop\work\DP\PJF_PV702_Genric\Localize1\%s\Dialog\%s'%(colName,text_name)
		# htmlf=open(type_name,mode='r',encoding="utf-8")
		# htmlcont=htmlf.read()
		# htmList=htmlcont.split('\n')
		# htmList[0]=htmList[0].replace("'",'"')
		# print(htmList[0])
		# s='\n'.join(htmList)
		# fp=open(r'C:\Users\Xuexiaobo\Desktop\work\DP\PJF_PV702_Genric\Localize\%s\Dialog\%s'%(colName,text_name),mode='w',encoding="utf-8")
		# fp.write(s)
		# fp.close()

def biaodian(newname):
		type_name=r'%s'%(newname)
		htmlf=open(type_name,mode='r',encoding="utf-8")
		htmlcont=htmlf.read()
		htmList=htmlcont.split('\n')
		htmList[0]=htmList[0].replace("'",'"')
		print(htmList[0])
		s='\n'.join(htmList)
		fp=open(r'%s'%(newname),mode='w',encoding="utf-8")
		fp.write(s)
		fp.close()