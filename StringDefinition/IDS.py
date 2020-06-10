import pymysql
import os
from xml.etree.ElementTree import ElementTree,Element
import xml.dom.minidom
from xml.etree import ElementTree as ET
import pymysql
import xlrd
from openpyxl import load_workbook
from StringDefinition import str_paixu
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
def create_node(tag,property_map):
	element=Element(tag,property_map)
	return element
def add_child_node(nodelist,element):
	for node in nodelist:
		node.append(element)
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)
# ree = read_xml("1.xml")
# text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
def lan_id(lan):		
	tree = read_xml('dialog\%s\StringDefinition.xml'%(lan))
	L_string=tree.findall("String")
	#print(L_string)
	lan_id=[]
	for i_string in L_string:
		id=i_string.get('id')
		text=i_string.text
		#i_string.text='666'
		# print(id)
		# print(text)
		lan_id.append(id)
		#write_xml(tree, "out.xml")
	return(lan_id,L_string)
def biaozhun_id(bianzhunTxt):		
	tree = read_xml('%s'%(bianzhunTxt))
	L_string=tree.findall("String")
	#print(L_string)
	lan_id=[]
	for i_string in L_string:
		id=i_string.get('id')
		text=i_string.text
		#i_string.text='666'
		# print(id)
		# print(text)
		lan_id.append(id)
		#write_xml(tree, "out.xml")
	return(lan_id,L_string)
def stringDefinition(host,port,user,passwd,dbname,lan,bianzhunTxt,newname,replay):
	conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=dbname)
	cursor = conn.cursor()
	sql="SELECT Control_id FROM dialog_xml_ids"
	cursor.execute(sql) 
	conn.commit() 
	urlData = cursor.fetchall()
	idsList=[i[0] for i in urlData]
	tree = read_xml('%s'%(newname))
	root = tree.getroot()
	# for child in root:
		# print(root.getchildren())
	tag = root.tag
	#parent_nodes=tree.findall("StringDefinition")
	ENU_nodeList=tree.findall("String")
	#print(L_string)
	ENU_id=[]
	for i_string in ENU_nodeList:
		id=i_string.get('id')
		text=i_string.text
		#i_string.text='666'
		# print(id)
		# print(text)
		ENU_id.append(id)
		#write_xml(tree, "out.xml")
	JPN_id,JPN_nodeList=biaozhun_id(bianzhunTxt)
	JI_JPN_ENU_list=[item for item in ENU_id if item not in JPN_id]
	#print(JI_JPN_ENU_list)
	JI_node=[item for item in ENU_nodeList if item.get('id') in JI_JPN_ENU_list]
	#print(ENU_nodeList)
	#print(JI_node)
	#print(root)
	children=root.getchildren()
	#print(children)
	if replay==int(16384):
		for j in range(1,200):
			try:
				for child in JI_node:
					#print(child)
					root.remove(child)
			except:
				pass
	else:
		pass
		
	ZE_JPN_ENU_list=[item for item in JPN_id if item not in ENU_id]
	ZE_node=[item for item in JPN_nodeList if item.get('id') in ZE_JPN_ENU_list]
	#print(ZE_node)
	for child in ZE_node:
		#if child.get('id') in child
		root.append(child)
	#print(children)
	write_xml(tree, '%s'%(newname))
	tree_Replace = read_xml('%s'%(newname))
	L_string=tree_Replace.findall("String")

		
	for i in L_string:
		id=i.get('id')
		#print(id)
		#text=(i.text)
		quarySql="SELECT %s FROM dialog_xml_ids WHERE Control_id='%s'"%(lan,id)
		#print(quarySql)
		cursor.execute(quarySql) 
		conn.commit() 
		urlData = cursor.fetchall()
		#print(id)
		#print(urlData)
		if urlData==():
			if id in idsList:
				print(id)
			pass
		else:
			i.text=urlData[0][0]
			#print(i.text)
	write_xml(tree_Replace, '%s'%(newname))
	if replay==int(16384):
		str_paixu.paixu(bianzhunTxt,newname)
	else:
		pass
