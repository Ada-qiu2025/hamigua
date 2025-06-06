# encoding: utf-8

from mypackage.disPacher import *
import time, random
import logging.config, os
import mypackage.comm as cm
import mypackage.stateCenter as sc
import logging.handlers
import threadpool
from multiprocessing import Process

isdebug = True
# # logging初始化工作
# logging.basicConfig()
#
# # myapp的初始化工作
# myapp = logging.getLogger('root')
# myapp.setLevel(logging.DEBUG)
#
# # 添加TimedRotatingFileHandler
# # 定义一个1秒换一次log文件的handler
# # 保留3个旧log文件
# filehandler = logging.handlers.TimedRotatingFileHandler("logs/myapp.logs", when='S', interval=1, backupCount=3)
# # 设置后缀名称，跟strftime的格式一样
# filehandler.suffix = "%Y-%m-%d_%H-%M-%S.logs"
# myapp.addHandler(filehandler)


# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')


# 多个调度服务传图片,推药,审方等业务命令测试.
def mult_code_test():
    from multiprocessing import Pool
    rs = []
    doc_id = input('医生开始id:')
    test_times = int(input('测试次数:'))
    pool_num = int(input("进程池大小(医生数量):"))

    pool = Pool(processes=pool_num)
    for i in range(pool_num):
        rs.append(pool.apply_async(code_test,('code_test_doc:'+doc_id+i.__str__(),'code_test_mac:'+doc_id+i.__str__(), test_times)))
    pool.close()
    pool.join()

    photo_time = []
    drug_pushtime_li = []
    prescription_pushtime_li = []

    for i in rs:     # 统计每个医生
        photo_time.append(i.get()[0])
        drug_pushtime_li.append(i.get()[1])
        prescription_pushtime_li.append(i.get()[2])

    total = 0
    largest_time = 0
    error_count = 0
    for k in photo_time:
        for j in k:
            if j > largest_time:
                largest_time = j
            elif j > 5:
                error_count+=1
            total += j
    print('#================================#')
    print('总共图片上传测试次数:%d' % (len(photo_time)*len(k)))
    print('平均图片上传时间:%0.3f' % (total /(len(photo_time)*len(k))))
    print('最大上传时间:%0.3f' % largest_time)
    print('#================================#')

    total = 0
    largest_time = 0
    error_count = 0
    for k in drug_pushtime_li:
        for j in k:
            if j > largest_time:
                largest_time = j
            elif j > 5:
                error_count+=1
            total += j
    print('#================================#')
    print('总共推药测试次数:%d' % (len(photo_time) * len(k)))
    print('平均推药时间:%0.3f' % (total / (len(photo_time) * len(k))))
    print('最大推药时间:%0.3f' % largest_time)
    print('#================================#')


    total = 0
    largest_time = 0
    for k in prescription_pushtime_li:
        for j in k:
            if j > largest_time:
                largest_time = j
            total += j
    print('#================================#')
    print('总共审核测试次数:%d' % (len(photo_time) * len(k)))
    print('平均审核结果推送时间:%0.3f' % (total / (len(photo_time) * len(k))))
    print('最大审核结果推送时间:%0.3f' % largest_time)
    print('#================================#')


# 调度服务传图片,推药,审方等业务命令测试.
def code_test(doc_accout,mac,test_times=10):
    d = Doctor()
    st = Store()
    photo_time_li = []     # 传送图片地址的时间
    drug_pushtime_li = []   # 药品推送的时间
    prescription_pushtime_li = []   # 处方推送时间
    d.login(doc_accout)   # 医生登录

    for i in range(test_times):
        mac = mac + i.__str__()
        st.store_login(doc_accout, mac)
        time.sleep(2)

        # 医生接受业务, 取出医生收到命令的时间
        assert d.doc_status == Docstatus.DO_MATCH_SUCESS
        d.recevice('1001b')
        time.sleep(2)

        # 开始进行图片上传
        start_time = time.time()
        photo_url = 'http://www.cdfortis.com'+i.__str__()
        st.customsendfileparam(photo_url)

        for j in range(100):
            print('%s图片上传检测中,%d次.file_url:%s,d.callback_Event:%s' % (d.Account, j,d.file_url,d.callback_Event))
            if d.file_url == photo_url:  # and d.callback_Event == PharmacistCallbackEvent.PE_FILE_URL.value:
                break
            time.sleep(0.1)
        photo_time_li.append(time.time() - start_time)
        time.sleep(1)

        # 医生开始给用户推荐药品
        start_time = time.time()
        druginfo = '阿莫西伦胶囊,1天3次.按计量服用'+i.__str__()
        d.PharmacistPushDrug(druginfo)

        for j in range(100):
            print('%s推荐药品检测中,%d次.druginfo:%s,d.callback_Event:%s' % (d.Account, j, st.druginfo,d.callback_Event))
            if st.druginfo == druginfo:  # and st.callback_Event == CustomCallbackEvent.CE_PUSH_DRUG.value:
                break
            time.sleep(0.1)
        drug_pushtime_li.append(time.time() - start_time)
        time.sleep(1)

        # 医生开始给用户审核处方 
        start_time = time.time()
        prescr_rs = '审方不通过,理由:' + i.__str__()
        d.PharmacistPrescriptionCheckResult(prescr_rs)

        for j in range(100):
            print('%s审核处方检测中,%d次'%(d.Account,j))
            if st.prescription_rs == prescr_rs: # and st.callback_Event == CustomCallbackEvent.CE_PRESCRIPT_CHECK.value:
                break
            time.sleep(0.1)
        prescription_pushtime_li.append(time.time() - start_time)

        st.logout()
        time.sleep(5)
        print('医生:%s的第%d笔业务.'%(d.Account,i))
    return photo_time_li,drug_pushtime_li,prescription_pushtime_li


    # for i in range(test_times):
    #
    #     assert d.doc_status == Docstatus.DO_MATCH_SUCESS
    #     assert st.storestatus == Storestatus.ST_MATCH_SUCCESS
    #
    #     li.append(sc.find_Doc(doc_accout, 5, time.time(), 1000))  # 从药店登录开始计时.
    #     d.logout()
    #     st.logout()
    #
    #     assert d.doc_status == Docstatus.DO_OFFLINE
    #     assert st.storestatus == Storestatus.ST_OFFLINE


# 多个医生leave命令测试.
def mult_doc_leave_test():
    from multiprocessing import Pool
    rs = []
    doc_id = input('医生开始id:')
    test_times = int(input('测试次数:'))
    pool_num = int(input("进程池大小(医生数量):"))

    pool = Pool(processes=pool_num)
    for i in range(pool_num):
        rs.append(pool.apply_async(doc_leave_test,('leave_test_doc:'+doc_id+i.__str__(),'leave_test_mac:'+doc_id+i.__str__(), test_times)))
    pool.close()
    pool.join()

    total = 0
    largest_time = 0
    total_times = 0

    for i in rs:
        for j in i.get():
            total += j
            if j > largest_time:
                largest_time = j
                total_times += 1
    print('#================================#')
    print('总共测试次数:%d' % (pool_num*test_times))
    print('平均离开时间:%0.3f,总共时长:%d,统计个数:%0.3f' % (total / total_times,total,total_times))
    print('最大离开时间:%0.3f' % largest_time)
    print('#================================#')


# 医生leave命令测试
def doc_leave_test(doc_accout, mac, test_times):
    d = Doctor()
    st = Store()
    li = []

    for i in range(test_times):
        d.login(doc_accout)
        time.sleep(2)
        st.store_login(doc_accout, mac+i.__str__())

        time.sleep(2)
        assert d.doc_status == Docstatus.DO_MATCH_SUCESS
        assert st.storestatus == Storestatus.ST_MATCH_SUCCESS

        li.append(sc.find_Doc(doc_accout, 5, time.time(), 1000)) # 从药店登录开始计时.
        d.logout()
        st.logout()

        assert d.doc_status == Docstatus.DO_OFFLINE
        assert st.storestatus == Storestatus.ST_OFFLINE

    return li


# 药店拷机测试,随机做业务
def store_rd_running(mac, sleep_time=1):
    cu = Store()
    while True:
        doc_name = sc.getRdDoc()
        # 先找空闲医生,再找忙碌的医生
        if not doc_name:
            logging.info('药店:%s,开始寻找忙碌的医生' % mac)
            doc_name = sc.getRdDoc(2)

        if doc_name:
            cu.store_login(doc_name, mac)
            while True:
                time.sleep(sleep_time)
                is_end = random.randint(0, 10)
                if cu.storestatus in [Storestatus.ST_MATCH_SUCCESS, Storestatus.ST_WAIT]:
                    if is_end == 0:
                        cu.logout()
                    elif is_end == 10:
                        cu.logout()
                elif cu.storestatus == Storestatus.ST_OFFLINE:  # 未登录退出循环
                    break
                elif cu.storestatus == Storestatus.ST_BUSY:
                    if is_end in [0, 10]:
                        cu.logout()
                    elif is_end in [5, 7]:
                        cu.customsendfileparam('http://test.test.test')
        else:
            print("no doctor found")
            time.sleep(5)


# 多个药店随机做业务,不停止'''
def mult_store_rd_running(stroe_num):
    from multiprocessing import Process
    for i in range(stroe_num):
        p = Process(target=store_rd_running, args=(i.__str__(),))
        p.start()

# 医生拷机测试,随机做业务
def doc_rd_runing(docname, doc_type):
    '''单个医生随机做业务'''
    d = Doctor()
    if d.login(docname, doc_type):
        while True:
            workduring = 60  # 每次工作时间为1分钟
            sleeptime = 1  # 每次循环的时间
            leave_time = random.randint(1, 3) * 60  # 每次离开的时间
            leasetime = random.randint(1, 3) * 60  # 每次休息1-5分钟
            work_time = random.randint(10, 30) * 60  # 每次工作10-30分钟
            login_dur = random.randint(2, 5) * 60 * 60  # 每次登陆3-5分钟
            logout_dur = random.randint(10, 15) * 60  # 每次登出,休息3-5分钟

            time.sleep(sleeptime)
            if d.doc_status == Docstatus.DO_MATCH_SUCESS:
                d.recevice(b"101")
            elif d.doc_status == Docstatus.DO_BUSY:  # 检测工作状态
                d.PharmacistPushDrug('阿莫西林胶囊,1day once')
                d.PharmacistPrescriptionCheckResult('不通过,处方不合规')
                if (time.time() - d.startwort_time) > workduring:  # 工作时间超过60秒就关闭
                    d.endtask()
            elif d.doc_status == d.doc_status.DO_LEAVE:
                if (time.time() - d.leave_time) > leave_time:  # 离开超过时间就free
                    d.free()
            elif d.doc_status == Docstatus.DO_OFFLINE:
                d.login(docname, 4)

            # 检测暂离的状态
            if ((d.doc_status == 1 or d.doc_status == 2 or d.doc_status == 3 or d.doc_status == 4) and (
                        d.is_Pause == False) and (
                        (time.time() - d.PauseTime) > work_time)):
                d.pause(True)
            elif ((d.doc_status == 1 or d.doc_status == 2 or d.doc_status == 3 or d.doc_status == 4) and (
                        d.is_Pause == True) and (
                        (time.time() - d.PauseTime) > leasetime)):
                d.pause(False)

            if (time.time() - d.loginTime) > login_dur:
                d.logout()
                time.sleep(logout_dur)

# 多个医生拷机测试,随机业务  - 多进程
def multpro_doc_rd():
    '''多个医生随机做业务,不停止'''
    # DocLi = cm.getDocList()
    doc_num = int(input("医生数量:"))
    doc_id = int(input("医生开始ID号:"))
    print('//druggist_type 医生或药师类型 0中药师 1西药师 2执业中药师 3执业西药师 4医生')
    doc_type = int(input('医生的类型:'))
    for i in range(doc_num):
        p = Process(target=doc_rd_runing, args=('doctor_rd_bus:'+str(doc_id)+str(i),doc_type))
        p.start()

# 僵尸医生,医生接业务后,不操作.
def doc_always_busy(doc_name, doc_type=DocType.DO_TYPE_DOCTOR, need_strategy=Need_Strategy.STRATEGY_FIXED_DOC.value,
                    sleep_time=5 * 60):
    d = Doctor()
    d.login(doc_name, doctype=doc_type)

    store = Store()
    store.store_login(doc_name, doc_name, need_strategy=need_strategy)
    time.sleep(2)
    d.recevice()
    time.sleep(sleep_time)


# 多个僵尸医生
def mult_alays_busy():
    '''多个医生随机做业务,不停止'''
    DocNum = int(input("医生数量:"))
    start_id = int(input("起始ID:"))
    from multiprocessing import Process

    for i in range(DocNum):
        p = Process(target=doc_always_busy, args=('Doctor_always_busy:'+str(start_id)+str(i),))
        p.start()


def mult_alays_busy_druggist(doc_num=10, start_id=1):
    '''
    多个药师随机做业务,不停止
    '''
    # doc_num = int(input("药师数量:"))
    # start_id = int(input("起始ID:"))
    from multiprocessing import Process

    for i in range(doc_num):
        p = Process(target=doc_always_busy, args=(
            'druggist_always_busy:' + str(start_id) + str(i), DocType.DO_TYPE_DRUGGIST.value,
            Need_Strategy.STRATEGY_RD.value))
        p.start()


# 计算单个用户登录调度服务及状态转发的时间
def doc_logintime(doc_name):
    '''计算医生从登录到状态转发到状态中心中间的耗时'''
    d = Doctor()
    d.login(doc_name)
    login_time = sc.find_Doc(doc_name, 0, d.loginTime, 30)
    time.sleep(1)
    d.logout()
    logout_time = sc.find_Doc(doc_name, -1, time.time(), 30)
    return (login_time, logout_time)


# 计算多个用户登录调度服务及状态转发的时间
def mult_doc_logintime():
    from multiprocessing import Pool
    pool_num = int(input("进程池大小:"))
    doc_num = int(input("医生数量:"))
    run_times = int(input("迭代次数:"))

    pool = Pool(processes=pool_num)
    rs = []
    for j in range(run_times):
        for i in range(doc_num):
            rs.append(pool.apply_async(doc_logintime, (str(j) + str(i),)))
    pool.close()
    pool.join()

    # 计算平均值/最大登录时间等信息
    total_login = 0
    total_logout = 0
    max_login_time = 0
    max_logout_time = 0
    for i in rs:
        total_login += i.get()[0]
        total_logout += i.get()[1]
        if i.get()[0] > max_login_time:
            max_login_time = i.get()[0]
        if i.get()[1] > max_logout_time:
            max_logout_time = i.get()[1]

    print('----------------------------------------------------------')
    print('平均登录转发状态时间为:%0.3f' % (total_login / len(rs)))
    print('最大登录时间为:%0.3f' % (max_login_time))
    print('平均登出转发状态时间为:%0.3f' % (total_logout / len(rs)))
    print('最大登出时间为:%0.3f' % (max_logout_time))


# 单个用户排队并计算时间,该测试需要先调用僵尸医生模式.
def store_wait_time_test(mac, sleeptime=0, check_times=100):
    store = Store()
    doc_name = sc.getRdDoc(2)

    if doc_name:
        logging.debug('药店:%s,找到随机医生%s' % (mac, doc_name))
        store.store_login(doc_name, mac)

        logging.debug('药店:%s,开始寻找,药店状态:%s' % (mac, store.storestatus.__str__()))
        start_time = time.time()

        for i in range(check_times):
            if (store.storestatus == store.storestatus.ST_WAIT) or \
                            store.storestatus == store.storestatus.ST_OFFLINE:
                logging.debug('结束寻找,药店:%s,状态:%s,寻找次数:%d' % (mac, store.storestatus.__str__(), i))
                break
            time.sleep(0.1)
            logging.debug('未找到药店:%s,再次发起寻找,药店状态:%s,寻找次数:%d' % (mac, store.storestatus.__str__(), i))
        end_time = time.time()
        time.sleep(sleeptime)
        store.logout()  # 需要调用退出方法,否则会影响进程池下个进程
        return mac, start_time, end_time, end_time - start_time
    else:
        logging.error('没有可用的医生,%s'%mac)


# 多个用户排队时间计算
def mult_store_waittime_test():
    from multiprocessing import Pool
    pool_num = int(input("进程池大小:"))
    store_num = int(input("药店数量:"))
    wait_time = int(input("排队等待时间:"))

    pool = Pool(processes=pool_num)
    rs = []
    # for j in range(run_times):
    for i in range(store_num):
        rs.append(pool.apply_async(store_wait_time_test, (str(i), wait_time)))
    pool.close()
    pool.join()

    # cm.printResult(rs,'药店排队反馈')
    total_time = 0
    max_time = 0
    print('----------------------------------------------------------')
    for i in rs:
        print(i.get())
        total_time += i.get()[3]
        if i.get()[3] > max_time:
            max_time = i.get()[3]
    print('----------------------------------------------------------')
    print('平均排队时间为:%0.3f' % (total_time / len(rs)))
    print('最大排队时间为:%0.3f' % (max_time))
    print('----------------------------------------------------------')


if __name__ == '__main__':
    print('*****************************************************************************************************')
    print('1.医生拷机测试,业务随机    2.药店拷机测试,业务随机    3.持续业务医生   4.测试药店排队时间   5.测试医生登录登出时间 6.离开时间测试 7.命令推送测试')
    print('8.生成10个持续业务的药师')
    print('******************************************************************************************************')
    test_type = int(input("请选择测试类型:"))
    if test_type == 1:
        multpro_doc_rd()
    elif test_type == 2:
        stroe_num = int(input("药店数量:"))
        mult_store_rd_running(stroe_num)
    elif test_type == 3:
        mult_alays_busy()
    elif test_type == 4:
        # store_wait_time_test('00')
        print('请先使用3,开启多个忙碌医生.')
        mult_store_waittime_test()
    elif test_type == 5:
        mult_doc_logintime()
    elif test_type == 6:
        mult_doc_leave_test()
    elif test_type == 7:
        mult_code_test()
        # doc_leave_test('test_doc','mac',5)
    elif test_type == 8:
        mult_alays_busy_druggist()
    os.system('pause')
    #elif test_type == 6:
