# encoding: utf-8

from mypackage.disPacher import *
import time, random
import logging.config, os
import mypackage.comm as cm
import mypackage.stateCenter as sc
import logging.handlers
from multiprocessing import *

# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

def store_find_pharmist_check_prescription():
	cu = Store()
	for num in range(1,5):
		cu.store_login('wlj','mac',need_strategy=4,only_prescription_checking=1)
		time.sleep(2)
		if cu.storestatus in [Storestatus.ST_MATCH_SUCCESS, Storestatus.ST_WAIT, Storestatus.ST_BUSY]:
			time.sleep(60)
		else:
			pass
		print('loop %d times ' %num)

def mult_store_rd_running(stroe_num):
    from multiprocessing import Process

    for i in range(stroe_num):
        p = Process(target=store_find_pharmist_check_prescription)
        p.start()		
		
if __name__=='__main__':
	mult_store_rd_running(5)