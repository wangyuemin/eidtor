import pymysql
import os,sys
import os
import xlrd
import re
from bs4 import BeautifulSoup
import pymysql
L_dict={'CAT':'windows-1252','CHS':'GB2312','CHT':'Big5','CSY':'Windows-1250','DAN':'Windows-1252','DEU':'Windows-1252','ELL':'Windows-1253','ENU':'Windows-1252','ESP':'Windows-1252','FIN':'Windows-1252','FRA':'Windows-1252','HUN':'Windows-1250','ITA':'Windows-1252','JPN':'shift_jis','KOR':'ks_c_5601-1987','NLD':'Windows-1252','NOR':'Windows-1252','PLK':'Windows-1250','PTB':'Windows-1252','PTG':'Windows-1252','RUS':'Windows-1251','SVE':'Windows-1252','TRK':'Windows-1254'}
#txtNames=['IDH_MEDIA_SETTING_SIZE.htm']
def help_xingui(host,port,userdb,passwdb,dbname,lanName,txtname,helpshengchen_path,helpbianzhun_path):
		conn = pymysql.connect(host=host,port=port,user=userdb,passwd=passwdb,db=dbname)
		cursor = conn.cursor()
		bianzhun_lan=helpbianzhun_path.split('/')[-2]
		print(bianzhun_lan)
		print(lanName)
		htm_bodylf=open(r'%s/%s'%(helpbianzhun_path,txtname),mode='r',encoding=L_dict[bianzhun_lan])
		htm_bodylcont=htm_bodylf.read()
		htm_bodylcont=htm_bodylcont.replace('<b>','').replace('</b>','')
		title_sta=re.compile(r'\<TITLE>(.*?)\</TITLE>')
		title_duoyu=title_sta.findall(htm_bodylcont)[0]
		#print(title_duoyu)
		quarySql="SELECT %s FROM htm where %s='%s'"%(lanName,bianzhun_lan,title_duoyu)
		cursor.execute(quarySql) 
		conn.commit() 
		urlData = cursor.fetchall()
		title_new=urlData[0][0]
		#print(title_new)
		#print(htm_bodylcont)
		# soup= BeautifulSoup(htm_bodylcont,'html.parser')
		# h_soup=soup.htm_bodyl
		# head_tag = soup.body
		# #print(head_tag)
		# for child in head_tag.descendants:
			# print(child.string)
		duoyuList=['<span>','<font>','</font>','</span>']
		str_l=	htm_bodylcont.split('\n')
		#print(str_l[8:21])
		start_num=(str_l.index('<BODY>'))
		try:
			end_num=(str_l.index('</BODY>'))
		except:
			end_num=(str_l.index(' </BODY>'))
		p_numList=(str_l[start_num+1:end_num])
		txt_L=[]
		for p_num in p_numList:
			H_sta=re.compile(r'\<H1(.*?)\>')
			p_sta=re.compile(r'\<P(.*?)\>')
			span_sta=re.compile(r'\<span(.*?)\>')
			font_sta=re.compile(r'\<font(.*?)\>')
			H_duoyu=H_sta.findall(p_num)
			p_duoyu=p_sta.findall(p_num)
			span_duoyu=span_sta.findall(p_num)
			font_duoyu=font_sta.findall(p_num)
			for i in H_duoyu:
				p_num=p_num.replace(i,'')
			for i in p_duoyu:
				p_num=p_num.replace(i,'')
			for i in span_duoyu:
				p_num=p_num.replace(i,'')
			for i in font_duoyu:
				p_num=p_num.replace(i,'')
			for i in duoyuList:
				p_num=p_num.replace(i,'')
			p_num=(p_num.replace('</A> </P>','</A></P>'))
			if p_num==' <P>&nbsp;</P>' or p_num==' <P>　</P>':
				p_num=' <P style="margin-bottom:3.00pt;">&nbsp;</P>'
			else:
				pass
			#print(p_num)
			sta=re.compile(r'\>(.*?)\<')
			l_str=sta.findall(p_num)
			#print(l_str)
			
			for i in l_str:
				#print(i)
				#i=i.strip('[').strip(']')
				if i=='' or i==' ' or i=='&nbsp;':
					pass
				else:
					quarySql="SELECT %s FROM htm where %s='%s'"%(lanName,bianzhun_lan,i)
					cursor.execute(quarySql) 
					conn.commit() 
					urlData = cursor.fetchall()
					if urlData==():
						quarySql="SELECT %s FROM htm where %s='%s'"%(lanName,bianzhun_lan,i)
						cursor.execute(quarySql) 
						conn.commit() 
						urlData1 = cursor.fetchall()
						if urlData1==():
							print(i)
						else:
							shuziList=['1.','2.','3.','4.']
							if (i[0:2]) in ['1.','2.','3.','4.']:
								p_num=p_num.replace('%s<'%(i),'%s<'%(shuziList[shuziList.index(i[0:2])]+str(urlData1[0][0])))
								p_num=p_num.replace('[[','[')
								#p_num=shuziList[shuziList.index(i[0:2])]+p_num
								#print(p_num)
							else:
								if '注)' in i:
									quarySql_lan="SELECT %s FROM htm where id='900'"%(lanName)
									cursor.execute(quarySql_lan) 
									conn.commit() 
									urlData_lan = cursor.fetchall()
									p_num=p_num.replace('%s<'%(i),'%s<'%(str(urlData_lan[0][0])+str(urlData[0][0])))
									p_num=p_num.replace('[[','[')
								else:
									p_num=p_num.replace('%s<'%(i),'%s<'%(str(urlData1[0][0])))
									p_num=p_num.replace('[[','[')
								#print(p_num)
					else:
						if '注)' in i:
							quarySql_lan="SELECT %s FROM htm where id='900'"%(lanName)
							cursor.execute(quarySql_lan) 
							conn.commit() 
							urlData_lan = cursor.fetchall()
							p_num=p_num.replace('%s<'%(i),'%s<'%(str(urlData_lan[0][0])+str(urlData[0][0])))
							p_num=p_num.replace('[[','[')
						else:
							shuziList=['1.','2.','3.','4.']
							if (i[0:2]) in ['1.','2.','3.','4.']:
								p_num=p_num.replace('%s<'%(i),'%s<'%(shuziList[shuziList.index(i[0:2])]+str(urlData[0][0])))
								p_num=p_num.replace('[[','[')
								#p_num=shuziList[shuziList.index(i[0:2])]+p_num
							else:
								p_num=p_num.replace('%s<'%(i),'%s<'%(str(urlData[0][0])))
								p_num=p_num.replace('[[','[')
						#print(str(urlData[0][0]))
						#print(p_num)
			#print(p_num)
			txt_L.append(p_num)
		txt_L1=[]
		for i in txt_L:
			if i !=' ' or i !='&nbsp;' or i !=' ':
				txt_L1.append(i)
			else:
				pass
		zongList=str_l[0:start_num+1]+txt_L1+str_l[end_num:]
		zongList[3]=' <TITLE>%s</TITLE>'%(title_new)
		s='\n'.join(zongList)
		if os.path.exists('%s/%s/HELP'%(helpshengchen_path,lanName)):
			pass
		else:
			try:
				os.mkdir('%s/%s/HELP'%(helpshengchen_path,lanName))
			except:
				os.mkdir('%s/%s'%(helpshengchen_path,lanName))
				os.mkdir('%s/%s/HELP'%(helpshengchen_path,lanName))
		s=s.replace('%s'%(L_dict[bianzhun_lan]),'%s'%(L_dict[lanName]))
		fp=open(r'%s/%s/HELP/%s'%(helpshengchen_path,lanName,txtname),mode='w',encoding='%s'%(L_dict[lanName]),errors='ignore')
		fp.write(s)
		fp.close()
			
	#print(p_num)
	
	
'''	
sta=re.compile(r'\>(.*?)\<')
l_str=sta.findall(htm_bodylcont)
#print(l_str)
l=[]
for j in l_str:
	if j=='&nbsp;' or j=='' or j==' ':
		pass
	else:
		quarySql="SELECT * FROM htm_new where JPN='%s'"%(j)
		cursor.execute(quarySql) 
		conn.commit() 
		urlData = cursor.fetchall()
		if urlData==():
			print(j)
		else:
		#print(urlData)
		value=urlData[0][1:]
		#print(j)
		l.append(j)
print(l)
'''
	