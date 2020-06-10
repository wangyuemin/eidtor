import pymysql
import os,sys
from bs4 import BeautifulSoup
from gevent import monkey; monkey.patch_all()
import gevent
import time
import re
#colList=['CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
def storeData(cursor,namesFile,file_name,p,wTitle,wTitle_text):
	##print(value)
	#conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	wTitle=str(wTitle).replace('"','\\"').replace("'","\\'")
	wTitle_text=str(wTitle_text).replace('"','\\"').replace("'","\\'")
	#print(wTitle)
	try:
		sql = "INSERT INTO %s (url,title,langauge,context) VALUES('%s','%s','%s','%s')"%(namesFile,str(file_name),str(p),wTitle,wTitle_text)
		#print(sql)
		##print(namesFile,file_name,p,wTitle,wTitle_text)
		cursor.execute(sql) 
		conn.commit()
	except:
		sql = 'INSERT INTO %s (url,title,langauge,context) VALUES("%s","%s","%s","%s")'%(namesFile,str(file_name),str(p),wTitle,wTitle_text)
		#print(sql)
		##print(namesFile,file_name,p,wTitle,wTitle_text)
		cursor.execute(sql) 
		conn.commit()	
def insert(lanName,cursor,path_htm_body_p,L_dict):
	cursor.execute("drop table if exists %s"%lanName)
	createsql="create table IF NOT EXISTS %s (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`title` TEXT NULL,`langauge` TEXT NULL,`context` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"%lanName
	#print(createsql)
	cursor.execute(createsql) 
	conn.commit()
	files_names=r'%s\%s\HELP'%(path_htm_body_p,lanName) 
	LangeEncoding=L_dict['%s'%(lanName)]
	names=os.listdir(files_names) #apply.htm_body集合
	idNum=1
	for i in range(len(names)):
		file_name=names[i]#apply.htm_body
		htm_bodylf=open('%s\%s'%(files_names,file_name),mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
		htm_bodylcont=htm_bodylf.read()
		##print(htm_bodylcont)
		soup= BeautifulSoup(htm_bodylcont,'html.parser')
		h_soup=soup.htm_bodyl
		# p_t='%s_t'%(namesFile[txt_num])
		# p_title='%s_title'%(namesFile[txt_num])
		try:
			wTitle=soup.find_all('title')[0]
			wTitle_text=soup.find_all('title')[0].text
		except:
			wTitle=''
			wTitle_text=''
		storeData(cursor,lanName,file_name,'title',wTitle,wTitle_text)
		try: 
			wH1=soup.find_all('h1')[0]
			wH1_text=soup.find_all('h1')[0].text
		except:
			wH1=''
			wH1_text=''
		storeData(cursor,lanName,file_name,'h1',wH1,wH1_text)
		##print(wTitle,wH1)
		body=soup.body.contents
		bodyList=[]
		for j in body:
			if j!='\n' and j.name!='h1':
				bodyList.append(j)
		for tag in bodyList:
			tag_title=tag.name
			#print(tag_title)
			tag_context=str(tag)
			print(tag_context)
			if tag_title==None:
				sta=re.compile(r'\>(.*?)\<')
				duoyu=sta.findall(tag_context)
				print(duoyu)
			else:
				tagText=str(tag.text)
				#print('666')
				storeData(cursor,lanName,file_name,tag_title,tag_context,tagText)
def fenbie_table(host,port,dbName,path_htm_body_p):
	global conn 
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#print(path_htm_body_p)
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	#sqlnull="select count(*)  from sqlite_master where type='table' and name = '%s';"%()
	colList=os.listdir(path_htm_body_p)
	#namesFile=os.listdir(path_htm_body_p) #CHT
	namesFile=colList
	LTask=[]
	for lanName in namesFile:
		insert(lanName,cursor,path_htm_body_p,L_dict)
		# LTask.append(g)
	# #gevent.joinall(LTask)
	# for j in LTask:
		# j.join()

def storeData_union(value,cursor):
	#print(value)
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	try:
		sql = 'INSERT INTO htm (url,%s,%s,%s) VALUES("%s","%s","%s","%s")'%value
		#print(sql)
		##print(sql)
		cursor.execute(sql) 
		conn.commit()
	except:
		sql = "INSERT INTO htm (url,%s,%s,%s) VALUES('%s','%s','%s','%s')"%value
		#print(sql)
		##print(sql)
		cursor.execute(sql) 
		conn.commit()
def upData(cursor,value,dbName):
	#conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	try:
		sql1="UPDATE htm SET %s='%s',%s='%s',%s='%s' WHERE id='%s'"%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit()
	except:
		sql1='UPDATE htm SET %s="%s",%s="%s",%s="%s" WHERE id="%s"'%value
		#print(sql1)
		cursor.execute(sql1) 
		conn.commit() 
def quaryId(cursor,file_name):
	#conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	quarySql="SELECT * FROM htm WHERE url='%s'"%(file_name)
	cursor.execute(quarySql) 
	conn.commit() 
	urlData = cursor.fetchall()
	return(urlData[0][0])
def storecontext(cursor,url,colList,dbName):
	dict={}
	dict_lanuage={}
	maxnum=0
	for colName in colList:
		sql1="SELECT * FROM %s WHERE url='%s'"%(colName,url)
		cursor.execute(sql1) 
		conn.commit()
		urlData = cursor.fetchall()
		dict[len(urlData)]=urlData
		dict_lanuage[len(urlData)]=colName
		if len(urlData)>maxnum:
			maxnum=len(urlData)
	#print(dict[maxnum])
	#print(dict_lanuage[maxnum])
	p_t='%s_t'%(dict_lanuage[maxnum])
	p_title='%s_title'%(dict_lanuage[maxnum])
	#print(dict[maxnum])
	for k in range(len(dict[maxnum])):
		storeData_union((p_title,dict_lanuage[maxnum],p_t,dict[maxnum][k][1],dict[maxnum][k][2],dict[maxnum][k][3].replace('"','\\"').replace("'","\\'"),dict[maxnum][k][4].replace('"','\\"').replace("'","\\'")),cursor)
def insert_union(cursor,text_file,colList,dbName):
	num_dict=storecontext(cursor,text_file,colList,dbName)
	id=quaryId(cursor,text_file)
	for colName in colList:
		num_id=id
		p_t='%s_t'%(colName)
		p_title='%s_title'%(colName)
		sql1="SELECT * FROM %s WHERE url='%s'"%(colName,text_file)
		cursor.execute(sql1) 
		conn.commit()
		urlData = cursor.fetchall()
		for j in range(len(urlData)):
			addid=num_id+j
			upData(cursor,(p_title,urlData[j][2],colName,urlData[j][3].replace('"','\\"').replace("'","\\'"),p_t,urlData[j][4].replace('"','\\"').replace("'","\\'"),addid),dbName)
def table_union(host,port,dbName,path_htm_body_p):
	colList=os.listdir(path_htm_body_p)
	global conn
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#print(colList[0])
	sql='SELECT url FROM %s'%(colList[0])
	#print(sql)
	cursor.execute(sql) 
	conn.commit()
	urlData = cursor.fetchall()
	#print(urlData)
	urlList=[]
	for data in urlData:
		urlList.append(data[0])
	urlList = list(set(urlList))
	LTask=[]
	for text_file in urlList:
		#print(text_file)
		insert_union(cursor,text_file,colList,dbName)
		# LTask.append(g)
	# #gevent.joinall(LTask)
	# for j in LTask:
		# j.join()	

def htm(host,port,dbName,path_htm_body_p):
	fenbie_table(host,port,dbName,path_htm_body_p)
	table_union(host,port,dbName,path_htm_body_p)
#htm('db_test.db','Help')	