# encoding: utf-8
from mypackage.disPacher import *
import sys,os

def doc_busy():
    doc=Doctor()
    doc.login('lxq',4)
    time.sleep(1)
    store=Store()
    store.store_login(docname='lxq',mac='mac1',need_strategy=3)
    time.sleep(1)
    doc.recevice()
    time.sleep(999)

if __name__=='__main__':
    doc_busy()