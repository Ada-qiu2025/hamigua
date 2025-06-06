import os
import re

def parasLog():
    os.chdir('E:/Pydemo/python_test/python_test')
    fh = open("E:/Pydemo/python_test/python_test/log/receiveTime.log",'r')
    fh1 =fh.readlines()
    file_object = open('receiveTime.txt', 'w+')
    for line in fh1:
        sp1 = re.findall(r'[0-9]\.\d+', line )
        if sp1 :
            file_object.write(sp1[0]+'\n')
    fh.close()
    file_object.close()

if __name__ == '__main__':
    parasLog()