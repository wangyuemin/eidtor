import pymysql
import os
import pymysql
#path = r'.\PJF_PX753\Localize'
# namesFile=os.listdir(path)
# namesList=[]
# for file in namesFile:
	# if file!='Common':
		# namesList.append(file)

#HELP.ALI
def createHhc(dbName):
	conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	#sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"

	sqldialog_xml="CREATE TABLE `dialog_xml` (`id` INT NOT NULL AUTO_INCREMENT ,`url` TEXT NULL,`title` TEXT NULL,`Control_id` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
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
def creattable(dbName,path):
	createHhc(dbName)
	namesFile=os.listdir(path)
	namesList=[]
	for file in namesFile:
		if file!='Common':
			namesList.append(file)
	for file in namesList:

		addColumn('dialog_xml',file,dbName)
creattable('work',r'C:\Users\Xuexiaobo\Desktop\work\work\dialog')

