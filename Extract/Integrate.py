import pymysql
from itertools import combinations
dictTab={'e':'ENU','bp':'PTB','chs':'CHS','cht':'CHT','de':'DEU','es':'ESP','fr':'FRA','it':'ITA','kor':'KOR','j':'JPN','nld':'NLD','ptg':'PTG','rus':'RUS'}
def hebing(conn,cursor,dbName,makeDbName):
	sql='select id from %s.%s'%(dbName,makeDbName)
	print(sql)
	sql1='alter table %s.%s add column lanNum int(20) not null;'%(dbName,makeDbName)
	cursor.execute(sql1) 
	cursor.execute(sql)
	conn.commit()
	urlData = cursor.fetchall()
	#print(urlData)
	l=[i[0] for i in urlData]
	#l=['1']
	print(l)
	lType=[]
	Typedict={}
	numDict={}
	sql2='SHOW COLUMNS FROM %s.%s'%(dbName,makeDbName)
	cursor.execute(sql2) 
	conn.commit()
	urlData = cursor.fetchall()
	print(urlData)
	lLan=([item[0] for item in urlData])
	print(lLan)
	for i in l:
		sql='select * from %s.%s where id="%s"'%(dbName,makeDbName,i)
		cursor.execute(sql) 
		conn.commit()
		urlData = cursor.fetchall()
		#print(urlData)
		LNum=(list(urlData[0]))
		print(LNum)
		LNull=[]
		for num in range(len(LNum)):
			if LNum[num]!=None:
				LNull.append(lLan[num])
		if LNull not in lType:
			lType.append(LNull)
			Typedict[str(i)]=LNull
			numDict[str(i)]=len(LNull)
		sql="UPDATE %s.%s SET lanNum='%s' WHERE id='%s'"%(dbName,makeDbName,len(LNull),i)	
		cursor.execute(sql) 
		conn.commit()	
	#print(Typedict)
	print(LNull)
	numL=(list(numDict.values()))
	numL=list(set(numL))
	numL.sort(reverse=True)
	lanList=[]
	for num in numL:
		for i in lType:
			if len(i)==num:
				lanList.append(i)
	#print(lanList)
	sql='CREATE table local_xue select * from %s ORDER BY lanNum DESC;'%(makeDbName)
	sql1='drop table if exists %s'%(makeDbName)
	cursor.execute(sql) 
	cursor.execute(sql1)
	conn.commit()
	#print([item[1:-2] for item in lanList])
	lanyList=['any_value(%s)'%item for item in [item[1:-2] for item in lanList][0]]
	lanTxt=','.join(lanyList)+',any_value(tableName)'
	#print(lanTxt)#select JPN,ENU,any_value(CHS),count(JPN) count from local_xue group by JPN,ENU;
	Litem=[item[1:-2] for item in lanList][0]
	Litem.append('tableName')
	#print(lanList)
	print(Litem)
	for l in [item[1:-2] for item in lanList]:
		lan=','.join(l)
		try:
			sql='CREATE TABLE test12 (select %s from local_xue group by %s)'%(lanTxt,lan)
			sql0='drop table if exists local_xue'
			print(sql)
			cursor.execute(sql) 
			cursor.execute(sql0)
			conn.commit()
			print('1111111')
			for lan1 in Litem:
				print(lan1)
				sql="ALTER TABLE `test12` CHANGE COLUMN `any_value(%s)` `%s` LONGTEXT NULL "%(lan1,lan1)
				print(sql)
				cursor.execute(sql)
				conn.commit()
		except:
			sql='CREATE TABLE local_xue (select %s from test12 group by %s)'%(lanTxt,lan)
			sql0='drop table if exists test12'
			print(sql)
			cursor.execute(sql) 
			cursor.execute(sql0)
			conn.commit()
			for lan2 in Litem:
				sql="ALTER TABLE `local_xue` CHANGE COLUMN `any_value(%s)` `%s` LONGTEXT NULL "%(lan2,lan2)
				print(sql)
				cursor.execute(sql)
			conn.commit()
	try:
		sql='rename table local_xue to %s'%(makeDbName)
		cursor.execute(sql)
		conn.commit()	
	except:
		sql='rename table test12 to %s'%(makeDbName)
		cursor.execute(sql)
		conn.commit()
	sql6="ALTER TABLE %s.%s ADD id INT(4) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;"%(dbName,makeDbName)
	sql7="ALTER TABLE %s.%s CHANGE COLUMN `JPN` `JPN` LONGTEXT NULL AFTER `id`"%(dbName,makeDbName)
	sql8="ALTER TABLE %s.%s CHANGE COLUMN `ENU` `ENU` LONGTEXT NULL AFTER `JPN`"%(dbName,makeDbName)
	cursor.execute(sql6)
	cursor.execute(sql7)
	cursor.execute(sql8)
	conn.commit()		

def colNametest(host,port,dbNameList):
	dataListMax=[]
	Ldict={}
	dataList=[]
	for dbName in dbNameList:
		conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
		cursor = conn.cursor()
		sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = 'local' and table_schema = '%s'"%(dbName)
		cursor.execute(sql11) 
		conn.commit() 
		data = cursor.fetchall()
		dataList1=[item[0] for item in data if item[0] not in ['url','id','tableName']]
		#Ldict[dbName]=dataList1
		if len(dataList1)>len(dataListMax):
			Ldict[dbName]=dataList1
			dataListMax=dataList1
			maxName=dbName
	maxNum=len(dataListMax)
	for dbName in dbNameList:
		conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
		cursor = conn.cursor()
		sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = 'local' and table_schema = '%s'"%(dbName)
		cursor.execute(sql11) 
		conn.commit() 
		data = cursor.fetchall()
		dataList1=[item[0] for item in data if item[0] not in ['url','id','tableName']]
		#Ldict[dbName]=dataList1
		if len(dataList1)>len(dataList):
			#Ldict[dbName]=dataList1
			dataList=dataList1
			maxName=dbName
		lNum=[]
		if len(dataList1)<=maxNum:
			for j in range(len(dataListMax)):
				if dataListMax[j] in dataList1:
					lNum.append(dataListMax[j])
				else:
					lNum.append('null')
		Ldict[dbName]=','.join(lNum)
	datasql=','.join(dataList)
	return(datasql,maxName,Ldict)
def tabcolName(host,port,tableName):
	dbNamecell=tableName.split('+')[0]
	tableNamecell=tableName.split('+')[1]
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbNamecell))	
	cursor = conn.cursor()
	sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"%(tableNamecell,dbNamecell)
	cursor.execute(sql11) 
	conn.commit() 
	data = cursor.fetchall()
	dataList1=[item[0] for item in data if item[0] in ['CAT','JPN','ENU','CHS','CHT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']]
	return(dataList1)
def colName(host,port,dbNameList):
	dataListMax=[]
	Ldict={}
	dataList=[]
	for dbName in dbNameList:
		dbNamecell=dbName.split('+')[0]
		tableNamecell=dbName.split('+')[1]
		conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbNamecell))
		cursor = conn.cursor()
		sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"%(tableNamecell,dbNamecell)
		cursor.execute(sql11) 
		conn.commit() 
		data = cursor.fetchall()
		dataList1=[item[0] for item in data if item[0] in ['CAT','JPN','ENU','CHS','CHT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']]
		#print(dataList1)
		for i in dataList1:
			if i not in dataListMax:
				dataListMax.append(i)
		
		#Ldict[dbName]=dataList1
		# if len(dataList1)>len(dataListMax):
			# Ldict[dbName]=dataList1
			# dataListMax=dataList1
			# maxName=dbName
	#print(dataListMax)
	maxNum=len(dataListMax)
	for dbName in dbNameList:
		dbNamecell=dbName.split('+')[0]
		tableNamecell=dbName.split('+')[1]
		conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbNamecell))
		cursor = conn.cursor()
		sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'"%(tableNamecell,dbNamecell)
		cursor.execute(sql11) 
		conn.commit() 
		data = cursor.fetchall()
		dataList1=[item[0] for item in data if item[0] in ['CAT','JPN','ENU','CHS','CHT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']]
		#Ldict[dbName]=dataList1
		if len(dataList1)>len(dataList):
			#Ldict[dbName]=dataList1
			dataList=dataList1
			maxName=dbName
		lNum=[]
		if len(dataList1)<=maxNum:
			for j in range(len(dataListMax)):
				if dataListMax[j] in dataList1:
					lNum.append(dataListMax[j])
				else:
					lNum.append('null')
		#print(lNum)
		Ldict[dbName]=','.join(lNum)
	datasqlmax=','.join(dataListMax)
	return(datasqlmax,dataListMax,Ldict)
def searchDB(host,port,dbNameList,dbName):
	sqlList=[]
	datasqlmax,dataListMax,Ldict=colName(host,port,dbNameList)
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sqlde="DROP TABLE IF exists tb77889tb;"
	cursor.execute(sqlde)
	sqltb ="CREATE TABLE `tb77889tb` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	cursor.execute(sqltb) 

	for j in dataListMax:
		sql="ALTER TABLE `tb77889tb` ADD COLUMN `%s` TEXT NULL;"%(j)
		cursor.execute(sql) 
	conn.commit()
	#print(Ldict)
	# maxDb=maxName.split('+')[0]
	# maxTable=maxName.split('+')[1]
	# sqlmax="SELECT %s FROM %s.`%s`"%(sqltest,maxDb,maxTable)
	# sqlList.append(sqlmax)
	#colNamesql=colName(host,port,dbNameList)
	for i in dbNameList:
		#if i != maxName:
		DbName=i.split('+')[0]
		TableName=i.split('+')[1]
		sql="SELECT %s FROM %s.`%s`"%(Ldict[i],DbName,TableName)
		sqlList.append(sql)
	datasql1='SELECT %s FROM %s.`tb77889tb`'%(datasqlmax,dbName)+' UNION '+' UNION '.join(sqlList)
	return(datasql1)
def creatSql(host,port,dbNameList):
#l=[1,2,3,4,5]
	sql6=''
	for i in range(len(dbNameList),0,-1):
		#print(i)
		for j in (list(combinations(dbNameList, i))):
			print(list(j))
			
			sqlChaList=[]
			chaList=[item for item in dbNameList if item not in list(j)]
			sqllanList=[]
			
			sqlList=[]				
			for i in list(j):
				#print(i)

				for lan in (tabcolName(host,port,i)):
					
					sql='tempstable.%s in '%(lan)+"(SELECT %s from %s.%s)"%(lan,i.split('+')[0],i.split('+')[1])
					sqlList.append(sql)
					
					sql="'%s'"%(','.join(list(j)))
			print(sqlList)
			#datasql='when tempstable.JPN in '+' and tempstable.JPN in '.join(sqlList)+' then '+sql
		# for j in chaList:
			# sql1="(SELECT jpn from %s.%s)"%(j.split('+')[0],j.split('+')[1])
			# sqlChaList.append(sql1)
			# #print(sqlChaList)
			# chasql=('and tempstable.JPN not in ' +'and tempstable.JPN not in '.join(sqlChaList))
			# #print(chasql)
			# #sql="'%s'"%(','.join(list(j)))		
		# if sqlChaList!=[]:
			# datasql='when tempstable.JPN in '+' and tempstable.JPN in '.join(sqlList)+chasql+' then '+sql+' '
		# else:
			datasql='when '+(' and ').join(sqlList)+' then '+sql+' '
			print(datasql)
			sqllanList.append(datasql)
				#print(sqllanList)
			sqllan=''.join(sqllanList)
			print(sqllan)
		#' then '+sql+' '
			sql6=sql6+sqllan
	#print(sql6)
	return(sql6)
def creatSqltest(dbNameList):
#l=[1,2,3,4,5]
	sql6=''
	for i in range(len(dbNameList),0,-1):
		print(i)
		for j in (list(combinations(dbNameList, i))):
			#print(list(j))
			sqlList=[]
			print(j)
			for i in list(j):
				
				sql="(SELECT jpn from %s.local)"%(i)
				sqlList.append(sql)
				sql="'%s'"%(','.join(list(j)))
				datasql='when tempstable.JPN in '+' and tempstable.JPN in '.join(sqlList)+' then '+sql
			print(datasql)
			sql6=sql6+datasql
	#print(sql6)
	return(sql6)
def searchDBtest(host,port,dbNameList):
	sqlList=[]
	sqltest,maxName,Ldict=colNametest(host,port,dbNameList)
	print(sqltest)
	print(maxName)
	print(Ldict)
	sqlmax="SELECT %s FROM %s.`local`"%(sqltest,maxName)
	sqlList.append(sqlmax)
	#colNamesql=colName(host,port,dbNameList)
	for i in dbNameList:
		if i != maxName:
			sql="SELECT %s FROM %s.`local`"%(Ldict[i],i)
			sqlList.append(sql)
	datasql1=' UNION '.join(sqlList)
	return(datasql1)
def IntegrateTable(host,port,dbNameList,dbName,makeDbName):
	#print(dbNameList)
	print(dbName)
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql1="DROP TABLE IF exists tempstable;"
	#sql2="CREATE TEMPORARY TABLE tempstable (%s);"%(searchDB(host,port,dbNameList))
	sql2="CREATE TABLE tempstable (%s);"%(searchDB(host,port,dbNameList,dbName))
	sql3="DROP TABLE IF exists tb77889tb;"
	sql4="DROP TABLE IF exists %s.%s;"%(dbName,makeDbName)
	sql5="CREATE TABLE %s.%s(select %s ,case %s else 'False' end as tableName from tempstable)"%(dbName,makeDbName,colName(host,port,dbNameList)[0],creatSql(host,port,dbNameList))
	sql6="ALTER TABLE %s ADD id INT(4) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;"%(makeDbName)
	sql7="ALTER TABLE %s.%s CHANGE COLUMN `JPN` `JPN` LONGTEXT NULL AFTER `id`"%(dbName,makeDbName)
	sql8="ALTER TABLE %s.%s CHANGE COLUMN `ENU` `ENU` LONGTEXT NULL AFTER `JPN`"%(dbName,makeDbName)
	cursor.execute(sql1)
	#print(sql5)
	cursor.execute(sql2)
	cursor.execute(sql3)
	cursor.execute(sql4)
	cursor.execute(sql5)
	cursor.execute(sql6)
	cursor.execute(sql7)
	cursor.execute(sql8)
	conn.commit()
	print(66666666666)
	hebing(conn,cursor,dbName,makeDbName)
	
	
	
	
	
	# conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	# cursor = conn.cursor()
	# sql0="show tables;"
	# cursor.execute(sql0)
	# #conn.commit()
	# data = cursor.fetchall()
	# dataList1=[item[0] for item in data]
	# print(dataList1)
	# if 'hhc' not in dataList1:
		# sqlrc="select COLUMN_NAME from information_schema.COLUMNS where table_name = 'rc' and table_schema = '%s'"%(dbName)
		# sqlppd="select COLUMN_NAME from information_schema.COLUMNS where table_name = 'ppd' and table_schema = '%s'"%(dbName)
		# cursor.execute(sqlrc)
		# data = cursor.fetchall()
		# #conn.commit()
		# dataListrc=[item[0] for item in data if item[0] not in ['url','id','tab','title','Control_id']]
		
		# for tabRc in dataListrc:
			# try:
				# name=tabRc.split('_')[-1]
				# tabName=dictTab[name]
				# sql='ALTER TABLE rc CHANGE %s %s TEXT;'%(tabRc,tabName)
				# cursor.execute(sql)
			# except:
				# pass
		# #print(dataListrc)
		# cursor.execute(sqlppd)
		# #conn.commit()
		# data = cursor.fetchall()
		# dataListppd=[item[0] for item in data if item[0] not in ['url','id','tab','title','Control_id']]
		# datasql=','.join(dataListppd)
		# #print(datasql)
		# sql1="DROP TABLE IF exists tempstable"
		# #sql2="CREATE TEMPORARY TABLE tempstable (select %s FROM ppd UNION select %s FROM rc "%(datasql,datasql)
		# #sql3="CREATE TABLE local(select %s ,case when tempstable.JPN in(SELECT jpn from rc) then 'rc' when tempstable.JPN in(SELECT jpn from ppd) then 'ppd' when tempstable.JPN in(SELECT jpn from dialog_xml) then 'dialog_xml'  else 'False' end as tableName from tempstable)"%(datasql)
		# sql4="CREATE TEMPORARY TABLE tempstable (select %s from ppd where ENU IN (select ENU FROM ppd UNION select ENU FROM rc ) UNION select %s from rc where ENU IN (select ENU FROM ppd UNION select ENU FROM rc ))"%(datasql,datasql)
		# sql5="DROP TABLE IF exists local"	
		# sql6="CREATE TABLE local(select %s ,case when tempstable.ENU in(SELECT ENU from ppd) then 'ppd' when tempstable.ENU in(SELECT ENU from rc) then 'rc'  else 'False' end as tableName from tempstable)"%(datasql)
		# cursor.execute(sql1)
		# cursor.execute(sql4)
		# cursor.execute(sql5)
		# cursor.execute(sql6)	
		# conn.commit()
	# else:
		# sql11="select COLUMN_NAME from information_schema.COLUMNS where table_name = 'hhc' and table_schema = '%s'"%(dbName)
		# cursor.execute(sql11) 
		# conn.commit() 
		# data = cursor.fetchall()
		# dataList=[item[0] for item in data if item[0] not in ['url','id']]
		# datasql=','.join(dataList)
		# print(datasql)
		# sql1="DROP TABLE IF exists tempstable"
		# sql2="CREATE TEMPORARY TABLE tempstable (select %s from hhc where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition) UNION select %s from hhk where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition))"%(datasql,datasql)
		# sql3="CREATE TABLE local(select %s ,case when tempstable.JPN in(SELECT jpn from hhc) then 'hhc' when tempstable.JPN in(SELECT jpn from hhk) then 'hhk' when tempstable.JPN in(SELECT jpn from dialog_xml) then 'dialog_xml' when tempstable.JPN in(SELECT jpn from stringdefinition) then 'stringdefinition' else 'False' end as tableName from tempstable)"%(datasql)
		# sql4="CREATE TEMPORARY TABLE tempstable (select %s from hhc where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition) UNION select %s from hhk where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition) UNION select %s from stringdefinition where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition) UNION select %s from dialog_xml where JPN IN (select jpn FROM hhc UNION select jpn FROM hhk UNION select jpn FROM dialog_xml WHERE title NOT in ('Font','style') UNION select jpn FROM stringdefinition))"%(datasql,datasql,datasql,datasql)
		# sql5="DROP TABLE IF exists local"	
		# sql6="CREATE TABLE local(select %s ,case when tempstable.JPN in(SELECT jpn from hhc) then 'hhc' when tempstable.JPN in(SELECT jpn from hhk) then 'hhk' when tempstable.JPN in(SELECT jpn from dialog_xml) then 'dialog_xml' when tempstable.JPN in(SELECT jpn from stringdefinition) then 'stringdefinition' else 'False' end as tableName from tempstable)"%(datasql)
		# cursor.execute(sql1)
		# cursor.execute(sql4)
		# cursor.execute(sql5)
		# cursor.execute(sql6)	
		# conn.commit()

def IntegrateUnion(host,port,dbNameList,dbName):
	print(dbNameList)
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql1="DROP TABLE IF exists tempstable;"
	sql2="CREATE TEMPORARY TABLE tempstable (%s);"%(searchDBtest(host,port,dbNameList))
	#sql2="CREATE TABLE tempstable (%s);"%(searchDB(host,port,dbNameList))
	sql3="select * from tempstable;"
	sql4="DROP TABLE IF exists %s.localUnion;"%(dbName)
	sql5="CREATE TABLE %s.localUnion(select %s ,case %s else 'False' end as tableName from tempstable)"%(dbName,colNametest(host,port,dbNameList)[0],creatSqltest(dbNameList))
	sql6="ALTER TABLE %s.localUnion ADD id INT(4) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;"%(dbName)
	sql7="ALTER TABLE %s.localUnion CHANGE COLUMN `JPN` `JPN` LONGTEXT NULL AFTER `id`"%(dbName)
	sql8="ALTER TABLE %s.localUnion CHANGE COLUMN `ENU` `ENU` LONGTEXT NULL AFTER `JPN`"%(dbName)
	cursor.execute(sql1)
	print(sql5)
	cursor.execute(sql2)
	cursor.execute(sql3)
	cursor.execute(sql4)
	cursor.execute(sql5)
	cursor.execute(sql6)	
	cursor.execute(sql7)
	cursor.execute(sql8)
	conn.commit()
	hebing(conn,cursor)
		