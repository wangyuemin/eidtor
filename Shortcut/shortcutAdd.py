import pymysql
import os
from xml.etree.ElementTree import ElementTree,Element
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
import itertools
from collections import Counter
RowList=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
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
			if '&' in pf:
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
def get_count_by_counter(l):
    t1 = time.time()
    count = Counter(l)   #类型： <class 'collections.Counter'>
    t2 = time.time()
    print (t2-t1)
    count_dict = dict(count)   #类型： <type 'dict'>
    return count_dict
def kuaijie_biaozhun(biaozhuanTXT,shengchengTXT,L_quzhiID,L_quzhiTxt):
	CHS_list,CHS_dict,CHS_all_dict=xml_text(biaozhuanTXT)
	ENU_list,ENU_dict,ENU_all_dict=xml_text(shengchengTXT)
	for id_context in L_quzhiID:
		CHS_list.remove(id_context)
		CHS_dict.pop(id_context)
		CHS_all_dict.pop(id_context)
		ENU_list.remove(id_context)
		ENU_dict.pop(id_context)
		ENU_all_dict.pop(id_context)		
	#print(CHS_list)
	L_list_zong=[]

	for j in CHS_list:
		#print(ENU_all_dict[j])
		L_list_zong.append(ENU_all_dict[j].upper())
	
	L_list_zong.sort(key=lambda x:len(x))
	#print(L_list)
	kuaijie_dict={}
	shanchu_list=[]
	for tt in range(1,(len(L_list_zong)+1)):
		#print(len(L_list_zong))
		c=[]
		for str_context in L_list_zong:

			list_context=list(str_context.upper())
			c=c+list_context
		#print(c)
		d=[item for item in c if item not in fuhao_list and item not in L_quzhiTxt]
		#print(d)
		chuxian_dict=(get_count_by_counter(d))
		#print(shanchu_list)
		for item in shanchu_list:
			try:
				del chuxian_dict[item]
			except:
				pass
		chuxian_keys=(list(chuxian_dict.keys()))
		
		chuxian_values=(list(chuxian_dict.values()))

		duoge_num_list=(duoge(list(chuxian_dict.values()),1))
		#print(duoge_num_list)
		#print(kuaijie_dict)
		#print(len(kuaijie_dict))
		if chuxian_values!=[]:
			if duoge_num_list !=[]:
				for i in duoge_num_list:
					#print(i)
					#print(chuxian_keys[i])
					for txt in L_list_zong:
						if chuxian_keys[i] in txt.upper():
							#print(txt)
							#kuaijie_dict[txt]=chuxian_keys[i]
							kuaijie_dict[chuxian_keys[i]]=txt
							shanchu_list.append(chuxian_keys[i])
							L_list_zong.remove(txt)
							break
					break
			else:
				#print(chuxian_values)
				min_num=(sorted(chuxian_values)[0])
				duoge_num_list_num=(duoge(list(chuxian_dict.values()),min_num))
				#print(duoge_num_list_num)
				for i in duoge_num_list_num:
					#print(i)
					#print(chuxian_keys[i])
					for txt in L_list_zong:
						if chuxian_keys[i] in txt.upper():
							#print(txt)
							#kuaijie_dict[txt]=chuxian_keys[i]
							kuaijie_dict[chuxian_keys[i]]=txt
							shanchu_list.append(chuxian_keys[i])
							L_list_zong.remove(txt)
							break
					break
		else:
			last_context=L_list_zong[0]
			f=[item for item in RowList if item not in shanchu_list]
			#print(f)
			#print(f[0])
			#print(L_list_zong)
			#kuaijie_dict[last_context]='(&'+f[0]+')'
			kuaijie_dict['(&'+f[0]+')']=last_context
			shanchu_list.append(f[0])
			L_list_zong.remove(last_context)				
				
	#print(kuaijie_dict)
	ret_keys=(list(ENU_all_dict.keys()))
	ret_values=(list(ENU_all_dict.values()))
	ret_valuesUpper=[]
	for i in ret_values:
		ret_valuesUpper.append(i.upper())
	new_dict={}
	kuaijie_keys=list(kuaijie_dict.keys())
	kuaijie_values=list(kuaijie_dict.values())
	shouzimu_list=[]
	for j in range(len(kuaijie_values)):
		if kuaijie_values[j] in ret_valuesUpper:
			new_letter=kuaijie_keys[j]
			if new_letter not in shouzimu_list:
				if '(' not in new_letter:
					#duogeList=duoge(ret_valuesUpper,kuaijie_values[j])
					num=ret_valuesUpper.index(kuaijie_values[j])
					#for num in duogeList:
					shouzimu_list.append(new_letter)
					index_num=(ret_valuesUpper[num].index(new_letter))
					#print(ret_values[num])
					new_str = ret_values[num][:index_num]+'&'+ret_values[num][index_num:]
					#print(new_str)
					#print(ret_keys[num])
					new_dict[ret_keys[num]]=new_str
					ret_keys.remove(ret_keys[num])
					ret_values.remove(ret_values[num])
					ret_valuesUpper.remove(ret_valuesUpper[num])
				else:
					#if kuaijie_values[j]=='F'
					num=ret_valuesUpper.index(kuaijie_values[j])
					# duogeList=duoge(ret_valuesUpper,kuaijie_values[j])
					# for num in duogeList:
					if ':' in ret_values[num]:
						a=ret_values[num].rstrip(':')
						rl=':'
					elif '...' in ret_values[num]:
						a=ret_values[num].rstrip('...')
						rl='...'
					else:
						a=ret_values[num]
						rl=''
					new_str =a+new_letter+rl
					shouzimu_list.append(new_letter)
					new_dict[ret_keys[num]]=new_str
					ret_keys.remove(ret_keys[num])
					ret_values.remove(ret_values[num])
					ret_valuesUpper.remove(ret_valuesUpper[num])
	print(new_dict)
	return(CHS_list,new_dict)

#fileNameList=['DialogDefinition_(05)IDD_DIALOG_SAVE_SETTING.xml','DialogDefinition_(07)IDD_COLOR_MODE_MAIN.xml','DialogDefinition_(10)IDD_DIALOG_ADVANCED.xml','DialogDefinition_(29)IDD_DIALOG_SAVE_DRIVER_SET.xml','DialogDefinition_(39)IDD_DIALOG_OVERLAYEDIT_CUSTOM.xml','DialogDefinition_(41)IDD_DIALOG_OVERLAYEREGISTER_CUSTOM.xml']
def shortAdd(files_name,colName,newname,path_biaozhun):

		L_quzhiID=[]
		L_quzhiTxt=[]
		bianzhuan_name=r'%s/%s'%(path_biaozhun,files_name)
		write_name=r'%s'%(newname)
		bianzhuan_tree = read_xml('%s'%(bianzhuan_name))
		bianzhuan_root = bianzhuan_tree.getroot()
		bianzhuan_L_Control=[]
		for Control in bianzhuan_root.iter("Control"):

			bianzhuan_L_Control.append(Control)	
		write_tree = read_xml('%s'%(write_name))
		write_root = write_tree.getroot()
		write_L_Control=[]
		for Control in write_root.iter("Control"):

			write_L_Control.append(Control)	
		for i in range(len(bianzhuan_L_Control)):

			bianzhuan_text=(bianzhuan_L_Control[i].find("Text").text)
			write_text=(write_L_Control[i].find("Text").text)
			bianzhan_id=bianzhuan_L_Control[i].get("id")

			if bianzhuan_text!=None and write_text!=None:
				if '(&' in bianzhuan_text and '&' in write_text:
					L_quzhiTxt.append(write_text.split('&')[1][0])
					L_quzhiID.append(bianzhan_id)
		print(L_quzhiTxt)
		print(L_quzhiID)

		L_Control_biaozhun,L_context_dict=kuaijie_biaozhun(bianzhuan_name,write_name,L_quzhiID,L_quzhiTxt)
		for i in write_L_Control:
			id=i.get('id')
			text_nodes = get_node_by_keyvalue(find_nodes(write_tree, "Control"), {"id":"%s"%(id)})

			if id in L_Control_biaozhun:

				Text= i.find("Text")
				Text.text=L_context_dict[id]

		write_xml(write_tree, r'%s'%(newname))
