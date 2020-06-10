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
def CJKAdd(files_name,colName,newname,path_biaozhun):
		bianzhuan_name=r'%s/%s'%(path_biaozhun,files_name)
		write_name=r'%s'%(newname)
		bianzhuan_tree = read_xml('%s'%(bianzhuan_name))
		bianzhuan_root = bianzhuan_tree.getroot()
		bianzhuan_L_Control=[]
		for Control in bianzhuan_root.iter("Control"):
			#print(Control.tag, ":", Control.attrib)
			bianzhuan_L_Control.append(Control)	
		write_tree = read_xml('%s'%(write_name))
		write_root = write_tree.getroot()
		write_L_Control=[]
		for Control in write_root.iter("Control"):
			#print(Control.tag, ":", Control.attrib)
			write_L_Control.append(Control)	
		for i in range(len(bianzhuan_L_Control)):
			#id=bianzhuan_L_Control[i].get('id')
			bianzhuan_text=(bianzhuan_L_Control[i].find("Text").text)
			write_text=(write_L_Control[i].find("Text").text)
			print(bianzhuan_text)
			print(write_text)
			if bianzhuan_text!=None and write_text!=None:
				if '(&' in bianzhuan_text and '(&' not in write_text:
					#print(text)
					Text= write_L_Control[i].find("Text")
					Text.text=write_L_Control[i].find("Text").text+'(&'+bianzhuan_L_Control[i].find("Text").text.split('(&')[1].split('(&')[0]
		write_xml(write_tree, r'%s'%(write_name))