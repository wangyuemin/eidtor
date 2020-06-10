from Extract import hhc
from Extract import hhk
from Extract import dialog_xml
from Extract import stringdefinition
import time
from Extract import creattable
from Extract import store
from Extract import htm
from Extract import dialog_xml_font
import os
import multiprocessing
import pymysql

#dbName='languagedict'
# path_dialog_xml = r'PJF_PX760\Localize'
# path_hhc = r'.\PJF_PX753\Localize\Common\RBK\DP_Generated\HELP'
# path_hhk = r'.\PJF_PX753\Localize\Common\RBK\DP_Generated\HELP'
# path_htm= r'.\PJF_PX753\Localize\Common\RBK\DP_Generated\HELP'
# path_stringdefinition = r'.\PJF_PX753\Localize'
# tableNameList=['test1','heping_db']
def collect(host,port,dbName,path,L_check):
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456')
	cursor = conn.cursor()
	
	createsql='CREATE DATABASE %s'%(dbName)
	try:
		cursor.execute(createsql)
		conn.commit()
	except:
		pass
	
	# tableNameList=['hhc','hhk','stringdefinition','dialog_xml','dialog_xml_font','htm']
	for tableName in L_check:
		try:
			cursor.execute("drop table if exists %s"%tableName)
			conn.commit()
		except:
			pass
	conn = pymysql.connect(host=host,port=port,user='root',passwd='123456',db='%s'%(dbName))
	cursor = conn.cursor()
	starttime=time.time()
	path='%s\Localize'%(path)
	path_stringdefinition=path_dialog_xml=path
	path_htm=path_hhk=path_hhc='%s/Common/RBK/DP_Generated/HELP'%(path)
	creattable.creattable(host,port,dbName,path,L_check)
	# p1=multiprocessing.Process(target = hhc.hhc, args = (dbName,path_hhc,))
	# p2=multiprocessing.Process(target = hhk.hhk, args = (dbName,path_hhk,))
	# p3=multiprocessing.Process(target = stringdefinition.stringdefinition, args = (dbName,path_stringdefinition,))
	# p4=multiprocessing.Process(target = dialog_xml.dialog_xml, args = (dbName,path_dialog_xml,))
	# p5=multiprocessing.Process(target = dialog_xml_font.dialog_xml_font, args = (dbName,path_dialog_xml,))
	# p6=multiprocessing.Process(target = htm.htm, args = (dbName,path_htm,))
	# p_list=[p1,p2,p3,p4,p5,p6]
	# for p in p_list:
		# p.start()
	# for p in p_list:
		# p.join()
	if 'hhc' in L_check:
		hhc.hhc(host,port,dbName,path_hhc)
	if 'hhk' in L_check:
		hhk.hhk(host,port,dbName,path_hhk)
	if 'stringdefinition' in L_check:
		stringdefinition.stringdefinition(host,port,dbName,path_stringdefinition)
	if 'dialog_xml' in L_check:
		dialog_xml.dialog_xml(host,port,dbName,path_dialog_xml)
	if 'dialog_xml_font' in L_check:
		dialog_xml_font.dialog_xml_font(host,port,dbName,path_dialog_xml)
	if 'htm' in L_check:
		htm.htm(host,port,dbName,path_htm)
	endtime=time.time()
	costtime=endtime-starttime
	print(costtime)
	#store.storehtm(dbName)
def storeXls(host,port,dbNameList,dir_choose):
	for dbName in dbNameList:
		dbNamecell=dbName.split('+')[0]
		tableNamecell=dbName.split('+')[1]
		store.store_xls(host,port,dbNamecell,[tableNamecell],dir_choose)
#colList=['JPN','CHS','ENU','CHT','CAT','CSY','DAN','DEU','ESP','FIN','FRA','HUN','ITA','NLD','NOR','PLK','PTB','PTG','RUS','SVE','ELL','KOR','TRK']
# path_htm = r'C:\Users\Xuexiaobo\tongyong\PJF_PV701\Localize\Common\RBK\DP_Generated\HELP'
#start_time = time.time()
#print(start_time)
#htm_th.main(dbName,path_htm)
#htm_test.main(dbName,path_htm)
#end_time = time.time()
#costtime = float(end_time) - float(start_time)
#print(end_time)
#print(costtime)

# htm_p.htm_p(dbName,path_htm_p)
# stringdefinition.stringdefinition(dbName,path_stringdefinition)
#store_xls.store_xls(dbName,tableNameList)
