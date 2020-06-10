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
def change_node_text(nodelist, text, is_add=False, is_delete=True):
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
	for String in root.iter("String"):
		#print(String.tag, ":", String.attrib)
		L_Control.append(String.get('id'))
	return(L_Control)
def nodeDict(file_name):
	tree = read_xml('%s'%(file_name))
	root = tree.getroot()

	L_Control={}
	for String in root.iter("String"):

		L_Control[String.get('id')]=String
	return(L_Control)

def paixu(bianzhunTxt,newname):
	old_name=r'%s'%(bianzhunTxt)
	new_name=r'%s'%(newname)
	write_name=r'%s'%(newname)
	#write_name=r'C:\Users\Xuexiaobo\Desktop\各机型db\760\PJF_xX760\Localize\%s\Dialog\%s'%(colName,txt_name)
	tree1 = read_xml('%s'%(write_name))
	root1 = tree1.getroot()
	tree = read_xml('%s'%(write_name))
	root = tree.getroot()
	print(nodeControl(new_name))
	l=nodeControl(new_name)
	ControlsL=root
	while [item for item in root.iter("String")] !=[]:
		for i in root.iter("String"):
			print(i)
			ControlsL.remove(i)

	for j in nodeControl(old_name):
		ControlsL.append(nodeDict(new_name)[j])
	write_xml(tree, r'%s'%(newname))
# chaji=[item for item in nodeControl(old_name) if item not in nodeControl(new_name)]	
# print(chaji)
# for i in root.iter("String"):
	# #print(i.get('id'))
	# for j in chaji:
		# if i.get('id')==j:
			# [item for item in root.iter("Controls")][0].remove(i)
# for String in new_root.iter("String"):
	# if String.get('id') not in nodeControl(old_name):
		# print(String.get('id'))
		# [item for item in root.iter("Controls")][0].append(String)

#write_xml(tree, r"C:\Users\Xuexiaobo\Desktop\work\work\dialog\%s\dialog\%s"%(colName,txt_name))