import pymysql
import os
#path = r'.\PJF_PX753\Localize'
# namesFile=os.listdir(path)
# namesList=[]
# for file in namesFile:
	# if file!='Common':
		# namesList.append(file)

#HELP.ALI
def createHhc(host,port,dbName,L_check):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	#sql = "INSERT INTO %s VALUES%s"%(self.table,value)
	#sql = "CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`JPN` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqlhhc ="CREATE TABLE `hhc` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqlhhk = "CREATE TABLE `hhkValue1` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqlhhk1="CREATE TABLE `hhkValue2` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqlstringdefinition = "CREATE TABLE `stringdefinition` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqldialog_xml="CREATE TABLE `dialog_xml` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`title` TEXT NULL,`Control_id` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqldialog_xml_font="CREATE TABLE `dialog_xml_font` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`title` TEXT NULL,`Control_id` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	sqlhtm = "CREATE TABLE `htm` (`id` INT NOT NULL AUTO_INCREMENT,`url` TEXT NULL,`title` TEXT NULL,INDEX `id` (`id`))COLLATE='utf8_general_ci'ENGINE=InnoDB;"
	#print(sql)
	if 'hhc' in L_check:
		cursor.execute("drop table if exists hhc")
		cursor.execute(sqlhhc)
	if 'hhk' in L_check:
		cursor.execute("drop table if exists hhk;")
		cursor.execute("drop table if exists hhkValue1;")
		cursor.execute("drop table if exists hhkValue2;")
		cursor.execute("drop table if exists hhkall;")
		cursor.execute(sqlhhk)
		cursor.execute(sqlhhk1)
	if 'stringdefinition' in L_check:
		cursor.execute("drop table if exists stringdefinition")
		cursor.execute(sqlstringdefinition)
	if 'dialog_xml' in L_check:
		cursor.execute("drop table if exists dialog_xml")
		cursor.execute(sqldialog_xml)
	if 'dialog_xml_font' in L_check:
		cursor.execute("drop table if exists dialog_xml_font")
		cursor.execute(sqldialog_xml_font)
	if 'htm' in L_check:
		cursor.execute("drop table if exists htm")
		cursor.execute(sqlhtm)
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
def addColumn(host,port,table,lanuage,dbName):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	sql="ALTER TABLE `%s`ADD COLUMN `%s` TEXT NULL;"%(table,lanuage)
	cursor.execute(sql) 
	conn.commit()
#createTable()
def creattable(host,port,dbName,path,L_check):
	createHhc(host,port,dbName,L_check)
	namesFile=os.listdir(path)
	namesList=[]
	for file in namesFile:
		if file!='Common':
			namesList.append(file)
	for file in namesList:
		P_style='%s_style'%(file)
		P_exstyle='%s_exstyle'%(file)
		P_class='%s_class'%(file)
		if 'hhc' in L_check:
			addColumn(host,port,'hhc',file,dbName)
		if 'hhk' in L_check:
			addColumn(host,port,'hhkValue1','%s'%(file),dbName)
			addColumn(host,port,'hhkValue2','%s'%(file),dbName)
		if 'stringdefinition' in L_check:
			addColumn(host,port,'stringdefinition',file,dbName)
		if 'dialog_xml' in L_check:
			addColumn(host,port,'dialog_xml',file,dbName)
			addColumn(host,port,'dialog_xml',P_style,dbName)
			addColumn(host,port,'dialog_xml',P_exstyle,dbName)
			addColumn(host,port,'dialog_xml',P_class,dbName)
		if 'dialog_xml_font' in L_check:
			addColumn(host,port,'dialog_xml_font',file,dbName)
		if 'htm' in L_check:
			addColumn(host,port,'htm',file,dbName)
			addColumn(host,port,'htm','%s_t'%file,dbName)
			addColumn(host,port,'htm','%s_title'%file,dbName)
