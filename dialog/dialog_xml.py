import pymysql
import os
from xml.etree.ElementTree import ElementTree,Element


def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree
def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
       node: 节点
       kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True
def write_xml(tree, out_path):
    '''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8",xml_declaration=True)
def find_nodes(tree, path):
    '''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)
def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text
def get_node_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
       nodelist: 节点列表
       kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes
def dialog_new(host,port,user,passwd,dbname,files_name,colName,newname):
	#path = r'C:\Users\Xuexiaobo\Desktop\work\work\dialog_new'
	#namesFile=os.listdir(path)
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	#colList=os.listdir(r'C:\Users\Xuexiaobo\Desktop\work\work\dialog')
	conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=dbname)
	cursor = conn.cursor()
	files_name_pure=files_name.split(')')[1].split('.xml')[0]
	tree = read_xml('%s'%(newname))
	root = tree.getroot()
	L_Caption=tree.findall("Caption")
	L_Control=[]
	for Control in root.iter("Control"):
		L_Control.append(Control)
	quarySql="SELECT %s FROM dialog_xml_new WHERE url='%s' and Control_id='Caption'"%(colName,files_name_pure)
	cursor.execute(quarySql) 
	conn.commit() 
	urlData = cursor.fetchall()
	L_Caption[0].text=urlData[0][0]
	fuhaoList=['xx.xx','--',']','[','xxx']
	for i in L_Control:
		id=i.get('id')
		text=(i.find("Text").text)
		quarySql="SELECT %s FROM dialog_xml_new WHERE url='%s' and  Control_id='%s'"%(colName,files_name_pure,id)
		cursor.execute(quarySql) 
		conn.commit() 
		urlData = cursor.fetchall()
		if urlData==():
			if text != None and text not in fuhaoList and 'xxx' not in text and 'IDD' not in text:
				print(files_name_pure)
				print(text)
		else:
			if text=='':
				Text= i.find("Text")
				Text.text=urlData[0][0]
			else:
				if text[-1]==':':
					Text= i.find("Text")
					Text.text=urlData[0][0]+':'
				elif '...' in text:
					Text= i.find("Text")
					Text.text=urlData[0][0]+'...'
					#Text=urlData[0][0]
				else:
					Text= i.find("Text")
					Text.text=urlData[0][0]
	write_xml(tree, r"%s"%(newname))
def nodeControl(file_name):
	tree = read_xml('%s'%(file_name))
	root = tree.getroot()
	#print(('%s\%s'%(path,files_name_pure)))
	#print(tree)
	#L_Caption=tree.findall("Caption")
	#L_Font=tree.findall("Font")
	#print(L_Font[0].attrib)
	#L_Font[0].attrib={'666':'666'}
	L_Control=[]
	for Control in root.iter("Control"):
		#print(Control.tag, ":", Control.attrib)
		L_Control.append(Control.get('id'))
	return(L_Control)

def nodeAdd(files_name,colName,newname,path_biaozhun):
	old_name=r'%s'%(newname)
	new_name=r'%s/%s'%(path_biaozhun,files_name)
	print(new_name)
	write_name=r'%s'%(newname)
	tree = read_xml('%s'%(write_name))
	old_tree = read_xml('%s'%(old_name))
	old_root = old_tree.getroot()
	old_Control={}
	new_tree = read_xml('%s'%(new_name))
	new_root = new_tree.getroot()
			
	print(old_Control)
	root = tree.getroot()
	print(len(nodeControl(old_name)))	
	print(len(nodeControl(new_name)))
	# for i in nodeControl(old_name):
		# if i not in nodeControl(new_name):
			# print(i)
	chaji=[item for item in nodeControl(old_name) if item not in nodeControl(new_name)]	
	addji=[item for item in nodeControl(new_name) if item not in nodeControl(old_name)]	
	print(chaji)
	print(addji)
	for k in range(1,50):
		for i in root.iter("Control"):
			#print(i.get('id'))
			for j in chaji:
				if i.get('id')==j:
					[item for item in root.iter("Controls")][0].remove(i)

	for Control in new_root.iter("Control"):
		if Control.get('id') not in nodeControl(old_name):
			print(Control.get('id'))
			[item for item in root.iter("Controls")][0].append(Control)
	write_xml(tree, r"%s"%(newname))
def nodeDict(file_name):
	tree = read_xml('%s'%(file_name))
	root = tree.getroot()

	L_Control={}
	for Control in root.iter("Control"):

		L_Control[Control.get('id')]=Control
	return(L_Control)
#colList=os.listdir(r'C:\Users\Xuexiaobo\Desktop\work\work\dialog')
#nameList=['DialogDefinition_(07)IDD_COLOR_MODE_MAIN.xml','DialogDefinition_(39)IDD_DIALOG_OVERLAYEDIT_CUSTOM.xml','DialogDefinition_(41)IDD_DIALOG_OVERLAYEREGISTER_CUSTOM.xml']
#nameList=['DialogDefinition_(39)IDD_DIALOG_OVERLAYEDIT_CUSTOM.xml','DialogDefinition_(41)IDD_DIALOG_OVERLAYEREGISTER_CUSTOM.xml']
def paixu(files_name,colName,newname,path_biaozhun):
		old_name=r'%s/%s'%(path_biaozhun,files_name)
		new_name=r'%s'%(newname)
		write_name=r'%s'%(newname)
		#write_name=r'C:\Users\Xuexiaobo\Desktop\各机型db\760\PJF_xX760\Localize\%s\Dialog\%s'%(colName,txt_name)
		tree1 = read_xml('%s'%(write_name))
		root1 = tree1.getroot()
		tree = read_xml('%s'%(write_name))
		root = tree.getroot()
		print(nodeControl(new_name))
		l=nodeControl(new_name)
		ControlsL=[item for item in root.iter("Controls")][0]
		while [item for item in root.iter("Control")] !=[]:
			for i in root.iter("Control"):
				print(i)
				ControlsL.remove(i)

		for j in nodeControl(old_name):
			ControlsL.append(nodeDict(new_name)[j])
		write_xml(tree, r'%s'%(newname))
def dialog_change(host,port,user,passwd,dbname,files_name,colName,newname):
		conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=dbname)
		cursor = conn.cursor()
		files_name_pure=files_name.split(')')[1].split('.xml')[0]
		tree = read_xml(r"%s"%(newname))
		root = tree.getroot()
		L_Caption=tree.findall("Caption")
		L_Control=[]
		for Control in root.iter("Control"):
			L_Control.append(Control)
		#LangeEncoding=L_dict['%s'%(colName)]
		quarySql="SELECT %s FROM dialog_xml_change WHERE url='%s' and Control_id='Caption'"%(colName,files_name_pure)
		cursor.execute(quarySql) 
		conn.commit() 
		urlData = cursor.fetchall()
		if urlData==():
			pass
		else:
			print(urlData)
			L_Caption[0].text=urlData[0][0]
		for i in L_Control:
			id=i.get('id')
			text=(i.find("Text").text)
			quarySql="SELECT %s FROM dialog_xml_change WHERE url='%s' and  Control_id='%s'"%(colName,files_name_pure,id)
			cursor.execute(quarySql) 
			conn.commit() 
			urlData = cursor.fetchall()
			if urlData==():
				pass
			else:
				if text[-1]==':':
					Text= i.find("Text")
					Text.text=urlData[0][0]+':'
				elif '...' in text:
					Text= i.find("Text")
					Text.text=urlData[0][0]+'...'
					#Text=urlData[0][0]
				else:
					Text= i.find("Text")
					Text.text=urlData[0][0]

		write_xml(tree, r"%s"%(newname))