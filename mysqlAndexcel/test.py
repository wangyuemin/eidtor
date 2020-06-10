import pymysql
# xlrd 为 python 中读取 excel 的库，支持.xls 和 .xlsx 文件
# import xlrd
 
# openpyxl 库支持 .xlsx 文件的读写
from openpyxl.reader.excel import load_workbook
from builtins import int
import xlrd
def createHhc(dbName,tableName):
	conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	#sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"

	sqldialog_xml="CREATE TABLE `%s` (`id` INT NOT NULL AUTO_INCREMENT ,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"%(tableName)
	#print(sql)

	cursor.execute(sqldialog_xml)
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
def addColumn(table,lanuage,dbName):
	conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql="ALTER TABLE `%s`ADD COLUMN `%s` TEXT NULL;"%(table,lanuage)
	cursor.execute(sql) 
	conn.commit()
#createTable()
def creattable(tableName,dbName,namesList):
	createHhc(dbName,tableName)
	for file in namesList:
		if file !='id':
			addColumn(tableName,file,dbName)
 
#cur 是数据库的游标链接，path 是 excel 文件的路径
path='模板.xlsx'

# xlrd版本
#读取excel文件


# openpyxl版本
#读取excel文件
workbook = load_workbook(path)
#获得所有工作表的名字
sheets = workbook.get_sheet_names()
print(sheets)
#获得第一张表
dbName='test1'
conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',charset='utf8')
cursor = conn.cursor()
cursor.execute("drop database if exists %s"%dbName)
cursor.execute("create database %s"%dbName)
cursor.execute("use %s"%dbName)
for tableName in sheets:
	worksheet = workbook.get_sheet_by_name(tableName)
	Read_xls = xlrd.open_workbook(r'%s'%(path))
	Read_table = Read_xls.sheet_by_name(r'%s'%(tableName))
	rowNum=(len(Read_table.col_values(1)))
	cursor.execute("drop table if exists %s"%tableName)
	namesList=Read_table.row_values(1)
	creattable(tableName,dbName,namesList)
	for i in range(2,rowNum):
		ID_list=Read_table.row_values(i)
		print(len(ID_list))
		print(len(tuple(ID_list)))
		print(ID_list)
		l=[]
		for i in ID_list:
			i=str(i).replace('"','\"').replace("'","\'")
			l.append(i)
		#l=[str(i).replace('"','\"').replace("'","\'") for i in ID_list]
		namesList=tuple(namesList)
		value=tuple(l)
		print(namesList)
		value=tuple([tableName])+namesList+value
		# print(value)
		#sql = 'INSERT INTO dialog_xml_new (id,url,title,Control_id,JPN,ENU,DEU,ESP,FRA,ITA,RUS,CHS,CHT,CSY,DAN,ELL,FIN,HUN,KOR,NLD,NOR,PLK,PTB,PTG,SVE,TRK) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%value
		context1='%s,'*len(ID_list)
		context1=context1.strip(',')
		context2='"%s",'*len(ID_list)
		context21="'%s',"*len(ID_list)
		context2=context2.strip(',')
		context21=context21.strip(',')
		sql1='INSERT INTO %s ('+context1+') VALUES('+context2+')'
		sql2='INSERT INTO %s ('+context1+') VALUES('+context21+')'
		try:
			sql=sql1%value
			print(sql)
			#sql = 'INSERT INTO %s (%s,%s,%s,%s) VALUES("%s","%s","%s","%s")'%value
			cursor.execute(sql)
		except:
			sql=sql2%value
			print(sql)
			#sql = 'INSERT INTO %s (%s,%s,%s,%s) VALUES("%s","%s","%s","%s")'%value
			cursor.execute(sql)
conn.commit()
#conn.close()