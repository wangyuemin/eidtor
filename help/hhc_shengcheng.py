import pymysql
import os
import re
import html
from bs4 import BeautifulSoup

def hhc(host,port,user,passwdb,dbname,lanName,hhchhkshengchen_path,biaozhun_path,hhcname):
# ree = read_xml("1.xml")
# text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	conn = pymysql.connect(host=host,port=port,user=user,passwd=passwdb,db=dbname)
	cursor = conn.cursor()
	top='''<html>
	<!-- Sitemap 1.0 -->
	<object type="text/site properties">
	  <param name="SiteType" value="toc">
	  <param name="Window Styles" value="0x800027">
	  <param name="ExWindow Styles" value="0x100">
	</object>'''
	bottom='''      </ul>
		</ul>
	</ul>
	</html>'''
	text_name='%s/%s'%(biaozhun_path,hhcname)
	shengcheng_name='%s/%s/%s'%(hhchhkshengchen_path,lanName,hhcname)
	if os.path.exists('%s/%s'%(hhchhkshengchen_path,lanName)):
		pass
	else:
		os.mkdir('%s/%s'%(hhchhkshengchen_path,lanName))
	LangeEncoding=L_dict['%s'%(lanName)]

	htmlf=open(text_name,mode='r',encoding='%s'%(LangeEncoding),errors='ignore')
	htmlcont=htmlf.read()
	#print(htmlcont)
	soup= BeautifulSoup(htmlcont,'html.parser')
	h_s=soup.find_all("param")
	s_value=[]
	for j in range(len(h_s)):
		#print(len(h_s))
		#print(j)
		#print(row_num)
		#print(i['name'])
		if (h_s[j]['value'] not in ["toc","0x800027","0x100"]):
			s_value.append(h_s[j])  #s_value 
	for k in range(len(s_value)):
		#print(s_value[k])
		if (k%2):
			pass
			url_text=s_value[k]
			#print(url_text)
		else:
			quarySql="SELECT %s FROM hhc WHERE url='%s'"%(lanName,s_value[k+1]['value'])
			#print(quarySql)
			cursor.execute(quarySql) 
			conn.commit() 
			urlData = cursor.fetchall()
			print(s_value[k+1]['value'])
			print(urlData)
			s_value[k]['value']=urlData[0][0].replace(':','').replace('...','')
	try:
		f = open(r"%s"%(shengcheng_name),'w',encoding='%s'%(L_dict['%s'%(lanName)]))
		#print(LangeEncoding)
		L=soup.prettify().split('</object>')
		text=''
		for i in range(len(L)):
			if i==0:
				line=top+'\n'
			elif 'param' not in L[i]:
				line=bottom
				#line=re.sub('>[^>]*<','><',L[i].replace('\n',''))
			else:
				line=re.sub('>[^>]*<','><',L[i].replace('\n','')).strip()+'</object>\n'
			text+=line
			textf=text.replace('"/','"').replace('</li>','')
		print(text_name)
		f.write(textf) 
		f.close()
	except:
		f = open(r"%s"%(shengcheng_name),'w',encoding='utf-8')
		#print(LangeEncoding)
		L=soup.prettify().split('</object>')
		text=''
		for i in range(len(L)):
			if i==0:
				line=top+'\n'
			elif 'param' not in L[i]:
				line=bottom
				#line=re.sub('>[^>]*<','><',L[i].replace('\n',''))
			else:
				line=re.sub('>[^>]*<','><',L[i].replace('\n','')).strip()+'</object>\n'
			text+=line
			textf=text.replace('"/','"').replace('</li>','')
		print(text_name)
		f.write(textf) 
		f.close()
				# context_text=s_value[k]
				# print(context_text)
'''
			if (k%2):					
				quarySql="SELECT * FROM hhc WHERE url='%s'"%(url_text)
				cursor.execute(quarySql) 
				conn.commit() 
				urlData = cursor.fetchall()
				if urlData==():
					storeData((namesFile[txt_num],url_text,context_text))
				else:
					upData((namesFile[txt_num],context_text,url_text))

'''
# tree = read_xml('1.xml')
# quarySql="SELECT %s,id FROM dialog_xml WHERE JPN='%s'"%(pd)
# cursor.execute(quarySql) 
# conn.commit() 
# urlData = cursor.fetchall()
# text_nodes = get_node_by_keyvalue(find_nodes(tree, "Control"), {"id":"IDS_DMDPI_BASE"})
# change_node_text(text _nodes, "new text")

# #6. 输出到结果文件
# write_xml(tree, "out.xml")