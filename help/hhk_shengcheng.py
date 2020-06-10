import pymysql
import os
import re
import html
from bs4 import BeautifulSoup
path = r'.'
namesFile=os.listdir(path)

# ree = read_xml("1.xml")
# text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency":"chain3"})
def hhk(host,port,userdb,passwdb,dbname,lanName,hhchhkshengchen_path,biaozhun_path,hhkname):
	text_name='%s/%s'%(biaozhun_path,hhkname)
	shengcheng_name='%s/%s/%s'%(hhchhkshengchen_path,lanName,hhkname)
	L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
	conn = pymysql.connect(host=host,port=port,user=userdb,passwd=passwdb,db=dbname)
	cursor = conn.cursor()
	top='''<html>
	<!-- Sitemap 1.0 -->
	<object type="text/site properties">
	  <param name="SiteType" value="index">
	</object>
	<ul>'''
	bottom='''</ul>
	</html>'''
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
		if (h_s[j]['value'] not in ["toc","0x800027","0x100","index"]):
			s_value.append(h_s[j])  #s_value 
	for k in range(len(s_value)):
		if (k%3==0):
			quarySql="SELECT %s FROM hhk WHERE url='%s'"%(lanName,s_value[k+2]['value'])
			print(quarySql)
			cursor.execute(quarySql) 
			conn.commit() 
			urlData = cursor.fetchall()
			print(urlData)
			s_value[k]['value']= urlData[0][0].replace(':','').replace('...','')
			print(s_value[k])
			print(k)
		elif (k%3==1):
			quarySql="SELECT %s FROM hhk WHERE url='%s'"%(lanName,s_value[k+1]['value'])
			print(quarySql)
			cursor.execute(quarySql) 
			conn.commit() 
			urlData = cursor.fetchall()
			print(urlData)
			s_value[k]['value']= urlData[0][0].replace(':','').replace('...','')				
			print(s_value[k])
			print(k)
		elif (k%3==2):
			print(s_value[k])	#url
			print(k)
		
		else:
			pass
	try:
		f = open(r"%s"%(shengcheng_name),'w',encoding='%s'%(L_dict['%s'%(lanName)]))
		#print(LangeEncoding)
		L=soup.prettify().split('</object>')
		text=''
		for i in range(len(L)):
			if i==0:
				line=top+'\n'
			elif i==1:
				line=re.sub('>[^>]*<','><',L[i].replace('\n','').replace('<ul>','')).strip()+'</object>\n'
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
			elif i==1:
				line=re.sub('>[^>]*<','><',L[i].replace('\n','').replace('<ul>','')).strip()+'</object>\n'
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
		
