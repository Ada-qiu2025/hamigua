# -*-coding:utf-8-*-
import os
import re
import random

def parasLog():
    os.chdir('E:/Pydemo/python_test/python_test')
    fh = open("E:/Pydemo/python_test/python_test/log/int.log",'r')
    fh1 =fh.readlines()
    file_object = open('IntspendTime.txt', 'w+')
    for line in fh1:
        sp = re.findall(r'cost time (.*?)$', line, re.M|re.I)
        #sp1 = re.findall(r'[0-9]\.\d+', line )
        if sp:
            file_object.write('{}'.format(sp[0])+'\n')
    fh.close()
    file_object.close()

def setCateId():
    cateId = []
    with open('E:\Pydemo\python_test\python_test\log\cateId.dat', 'r') as df:
        for line in df:
            data=line.rstrip().split('\t')
            print(data)
            cateId.append(data[0])
    print(cateId)

def setChainId():
    chainId = []
    with open('E:\Pydemo\python_test\python_test\log\chainId.dat', 'r') as df:
        for line in df:
            data = line.rstrip()
            chainId.append(data)
        print(chainId)

def setStoreId():
    storeId = []
    with open('E:\Pydemo\python_test\python_test\log\storeId.dat', 'r') as df:
        for line in df:
            data = line.rstrip()
            storeId.append(data)
        print(storeId)

def setKeyWorlds():
    keyWorlds = []
    with open('E:\Pydemo\python_test\python_test\log\常用药品表.txt', 'r',encoding= 'utf-8') as df:
        for line in df:
            data = line.rstrip()
            keyWorlds.append(data)
        print(keyWorlds)

def doclist():
    doc = []
    with open('E:\Pydemo\python_test\python_test\log\doclogAcct.dat', 'r',encoding= 'utf-8') as df:
        for line in df:
            data = line.rstrip()
            doc.append(data)
        print(doc)


if __name__ == '__main__':
    doclist()