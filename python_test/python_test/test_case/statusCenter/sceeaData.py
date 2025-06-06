# -*-coding:utf-8-*-
import os ,sys
sys.path.append('E:\Pydemo\python_test\python_test')
import http
import json
import random
import urllib.request
import urllib.parse


headers={'Content-Type': 'text/html','charset':'utf-8','Connection': 'keep-alive'}
url1='http://www.sceea.cn/InformationOpenness/GetSunshineList?id=203&page='


def getData():
	for page in range(155):
		url=url1+"%s"%(page)
		print (url)
		conn=urllib.request.Request(url,headers=headers,method='POST')
		response=urllib.request.urlopen(conn)
		ret=response.read()
		ret=ret.decode('utf-8')
		with open('E:\Pydemo\python_test\python_test\scData.txt', 'a+',encoding='utf-8') as f:
			f.write(ret)

			
def tes1():
	conn = urllib.request.Request(url1,headers=headers,method='POST')
	response = urllib.request.urlopen(conn)
	page = response.read()
	page = page.decode('utf-8')
	print (page)
		
if __name__ == '__main__':
    getData()