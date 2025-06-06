# encoding: utf-8
import mypackage.disPacher
from multiprocessing import Process
from multiprocessing import pool
import time
from random import randint
import os
import logging.config


# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

#定义医生业务数和医生账号为字典类型
busimap = {}
d = mypackage.disPacher.Doctor()

def doc_always_busy(doc_name,run_times):
    d.login(doc_name, 2)
    print(doc_name,d.doc_status)
    time.sleep(2)
    busi = 0
    for j in range(run_times):
        if d.doc_status==d.doc_status.DO_MATCH_SUCESS or d.doc_status==d.doc_status.DO_BUSY:
            d.recevice()
            busi+=1
            busimap['doc%s'%doc_name]=busi
            print(busimap)
            time.sleep(2)
            d.endtask()
            d.free()
    return busi


# 多个僵尸医生
def pool_doc():
    from multiprocessing import Pool
    rs = []
    doc_num = int(input("医生数量:"))
    pool = Pool(processes = int(input("进程池大小:")))
    run_times = int(input("迭代次数:"))
    doc_id=int(input("医生开始的id:"))
    for i in range(doc_num):
        doc_name= doc_id+i
        print("医生账号：%s"%doc_name)
        rs.append(pool.apply_async(doc_always_busy,args=(doc_name.__str__(),run_times,)))
    pool.close()
    pool.join()

    nums = []
    for res in rs:
        nums.append(res.get())  # 拿到所有结果
    print(nums)  # 主进程拿到所有的处理结果,可以在主进程中进行统一进行处理

    #计算方差
    ex = float(sum(nums)) / len(nums)
    s = 0
    for i in nums:
        s += (i - ex) ** 2
    f = float(s) / len(nums)
    print("方差:{0:2f}".format(f))

store=mypackage.disPacher.Store()
def Running(mac):
    '''药店请求药师，业务保持随机20以内，然后退出登录'''
    doclist = "|".join(str(i) for i in range(10))
    if (store.storestatus==store.storestatus.ST_OFFLINE):
        store.store_login1(doclist,mac,7)
        time.sleep(2)
        store.endtask()
        store.logout()

def mutiStore():
    '''多进程，药店请求随机业务'''
    number = int(input("input the store number:"))
    for i in range(number):
        mac = 'MAC'+ i.__str__()
        p = Process(target=Running, args=(mac,))
        p.start()

import time
from random import randint
from multiprocessing import Process


result=['0','pass', 'failed']

doc = mypackage.disPacher.Doctor()
cu = mypackage.disPacher.Store()

def pres_checking(docname,runtimes):
    time.sleep(1)
    doc.login(docname, 2)
    cu.store_login(mac='mac'+docname, need_strategy=7, docname=docname)
    doc.free()
    doc.recevice()
    time.sleep(1)
    i=randint(1,2)
    t1 = time.time()
    t = doc.pres_check(result[i])
    if (t==0):
        time.sleep(0.5)
        if (cu.callback_Event==12):
            t2=cu.callback_Time
            prestime=t2-t1
            print('{:.10f}'.format(prestime))
            print('send the result is ''%s'%result[i])
            time.sleep(1)
            doc.endtask()
            time.sleep(1)
            doc.logout()
            time.sleep(2)
            return prestime
    else:
        print(t)
        raise Exception('pres_check exception')

def mutipres_checking():
    DocNum = int(input("Doctor Total Num:"))
    DocId = int(input("Doctor Id:"))
    runtimes=int(input('runtimes:'))
    pool_num=int(input('进程池大小:'))

    from multiprocessing import Pool

    pool = Pool(processes=pool_num)
    spendtime = []

    for j in  range(runtimes):
        for i in range(DocNum):
            docname='%s'%(DocId+i)
            p=pool.apply_async(func=pres_checking,args=(docname,runtimes),)
            spendtime.append(p)
    pool.close()
    pool.join()

    nums = []
    for res in spendtime:
        m=res.get()
        if ( m is not None):
            nums.append(m)
    print(nums)

    # 计算审方的平均时间
    avgtime=sum(nums)/len(nums)
    print('-'*30)
    print('平均审方时间为:%0.7f' % avgtime)
    print('-'*30)

def druggist_always_pres_checking(docname,runtimes):
    doc.login(docname, 2)
    time.sleep(2)
    while True:
        time.sleep(2)
        print(doc.doc_status)
        if doc.doc_status==doc.doc_status.DO_MATCH_SUCESS or doc.doc_status==doc.doc_status.DO_FREE:
            doc.recevice()
            time.sleep(1)
            t1= doc.startwort_time #开始业务时间 (第一次业务开始时间)
            print('t1 time %s'%t1)
            doc.pres_check(result[randint(1,2)])
            time.sleep(1)
            # if (doc.callback_Event==4):#event=4 代表客户端主动结束业务
            #     t2 =doc.callbackEnd_Time #上一笔业务的结束时间
            #     print('t2 time %s' % t2)
            doc.endtask()
            t2 =time.time()
            doc.free()
            time.sleep(2)
        else:
            print("match failed")

from  mypackage import stateCenter

def doc_end_free(docname):
    doc.login(docname,2)
    time.sleep(2)
    if doc.doc_status==doc.doc_status.DO_MATCH_SUCESS or doc.doc_status.DO_FREE:
        doc.recevice()
        time.sleep(2)
        doc.endtask()
        doc.free()
        t1=stateCenter.find_Doc(docname,0)
        print(t1)
        return t1

def muti_doc_end_free():
    DocNum = int(input("Doctor Total Num:"))
    DocId = int(input("Doctor Id:"))
    runtimes = int(input('迭代次数:'))
    pool_num = int(input('进程池大小:'))
    sptime=[]

    from multiprocessing import Pool
    pool = Pool(processes=pool_num)
    for j in range(runtimes):
        for i in range(DocNum):
            docname = '%s' % (DocId + i)
            p=pool.apply_async(doc_end_free,(docname,) )
            sptime.append(p)
    pool.close()
    pool.join()

    nums=[]
    for res in sptime:
        m = res.get()
        if m is not None:
            nums.append(m)
    print(nums)

    # 计算审方的平均时间
    avgtime = sum(nums) / len(nums)

    print('*'*30)
    print('时间: %s'%avgtime)
    print('*' * 30)


def muti_druggist_checking():
    DocNum = int(input("Doctor Total Num:"))
    DocId = int(input("Doctor Id:"))
    runtimes = int(input('迭代次数:'))
    pool_num = int(input('进程池大小:'))

    from multiprocessing import Pool

    pool = Pool(processes=pool_num)
    for j in range(runtimes):
        for i in range(DocNum):
            docname = '%s' % (DocId + i)
            pool.apply_async(func=druggist_always_pres_checking, args=(docname, runtimes), )
    pool.close()
    pool.join()


if __name__ == '__main__':
    doc_end_free('lxq')





