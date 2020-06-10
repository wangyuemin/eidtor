import pymysql
import os,sys
from bs4 import BeautifulSoup
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from gevent import monkey; monkey.patch_all()
import gevent
import time
import pymysql
import os,sys
from bs4 import BeautifulSoup
import os
import xml.dom.minidom
from xml.etree import ElementTree as ET
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
from xml.etree.ElementTree import ElementTree,Element
#path_dialog_xml = r'.\PJF_PX753\Localize'
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
def read_xml(in_path):
    '''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def xml_text(text_name):
	#text_name='ENU.xml'
	tree = read_xml(text_name)
	dom = xml.dom.minidom.parse(text_name)
	root = dom.documentElement
	tagControl = root.getElementsByTagName('Control')
	num1=0

	list_id=[]
	for b in tagControl:
		#print (b.nodeName)
		pd=b.getAttribute("id")
		#print(pd)
		list_id.append(pd)					#control_id
		num1+=1
	per=ET.parse(text_name)
	p=per.findall('Controls')
	#print(p)
	#print(len(tagControl))
	biaozhun_id=[]
	biaozhun_dict={}
	all_dict={}
	for k in range(num1):
		node=list(p[0])[k]
		#print(node)
		root = dom.documentElement
		
		pd=list_id[k]
		#print(pd)
		#print(list(node)[0].text)
		pf=list(node)[0].text
		#print(pf)
		if pf != None:
			all_dict[pd]=pf
			if '&' in pf and '°' not in pf:
				biaozhun_id.append(pd)
				biaozhun_dict[pd]=pf
	return(biaozhun_id,biaozhun_dict,all_dict)
	#文本
	# pstyle=list(node)[1].text
	# print(pstyle)	#style	
	# pExStyle=list(node)[2].text
	# print(pExStyle)	#ExStyle
	# pClass=list(node)[3].text
	# print(pClass)	#Class
fuhao_list=[':','.',' ','-']
def num(txt):
	num=0
	for k in txt:
		if k not in fuhao_list:
			num=num+1
	#print(num)
	return(num)
def duoge(L,txt):
	Llist=[]
	for i in range(len(L)):
		if L[i]==txt:
			Llist.append(i)
	return (Llist)
def kuaijie_biaozhun(biaozhuanTXT,shengchengTXT):
	CHS_list,CHS_dict,CHS_all_dict=xml_text(biaozhuanTXT)
	ENU_list,ENU_dict,ENU_all_dict=xml_text(shengchengTXT)
	#print(CHS_list)
	L_list=[]
	new_dict={}
	print(CHS_list)
	for j in CHS_list:
		print(j)

		listTxt=CHS_all_dict[j]
		kuaijie=listTxt.split('&')[1].split(')')[0]	
		print(kuaijie)
		#print(ENU_all_dict[j])
		print(biaozhuanTXT,shengchengTXT)
		print(ENU_all_dict)
		txt=ENU_all_dict[j]
		if txt=='&X:' or txt=='&Y:':
			pass
		else:
			if ':' in txt:
				a=txt.rstrip(':')
				rl=':'
			elif '...' in txt:
				a=txt.rstrip('...')
				rl='...'
			else:
				a=txt
				rl=''
			print(a)
			if '(' in kuaijie:
				new_str ='&'+a+rl
				new_dict[j]=new_str
			else:
				if '(&' in a:
					new_str =a+rl
					new_dict[j]=new_str
				else:
					new_str =a+'(&'+kuaijie+')'+rl
					new_dict[j]=new_str
				#print(new_str)
			print(new_dict)
	return(CHS_list,new_dict)
#colList=os.listdir(r'C:\Users\Xuexiaobo\Desktop\work\work\dialog')
#nameList=['DialogDefinition_(00)IDD_SLP_ADD_MAIN.xml']
def CJKshortcut(files_name,colName,newname,path_biaozhun):
	biaozhuanTXT=r'%s/%s'%(path_biaozhun,files_name)
	shengchengTXT=r'%s'%(newname)
	#print(kuaijie_biaozhun(biaozhuanTXT,shengchengTXT))

	tree = read_xml(r'%s'%(newname))
	root = tree.getroot()
	L_Control=[]
	for Control in root.iter("Control"):
		#print(Control.tag, ":", Control.attrib)
		L_Control.append(Control)
	L_Control_biaozhun,L_context_dict=kuaijie_biaozhun(biaozhuanTXT,shengchengTXT)
	for i in L_Control:
		id=i.get('id')
		text_nodes = get_node_by_keyvalue(find_nodes(tree, "Control"), {"id":"%s"%(id)})
		#print(L_context_dict)
		if id in L_Control_biaozhun:
			#print(id)
			Text= i.find("Text")
			#print(L_context_dict)
			if Text.text=='&X:' or Text.text=='&Y:' or Text.text=='ID':
				pass
			else:
				Text.text=L_context_dict[id]
			#print(L_context_dict[id])
			#print(Text.text)
			#Text=urlData[0][0]
		#print(tree)
	write_xml(tree, r'%s'%(newname))


			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			