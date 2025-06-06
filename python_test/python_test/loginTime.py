# encoding: utf-8

import logging.config
import time
from multiprocessing import *

import test_case.dispatchcenter.disPacher

storeli = test_case.dispatchcenter.disPacher.getstorelist()
docli = test_case.dispatchcenter.disPacher.getDoclist()

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')


def run(mac, docaccount, doc=None):
    # print(docaccount)
    # doc = test_case.dispatchcenter.disPacher.Doctor(docaccount)
    # doc.login()
    # doc.pause(True)
    #
    # time.sleep(3)
    # store = test_case.dispatchcenter.disPacher.Store(mac)
    # store.store_login(docaccount, 3)
    # time.sleep(20)
    store = test_case.dispatchcenter.disPacher.Store(mac)
    store.store_login(docaccount, 3)
    time.sleep(3)


# run(storeli[5],docli[800])
if __name__ == '__main__':
    while True:
        for i in range(400, 420):
            p = Process(target=run, args=(storeli[i],docli[i]))
            p.start()
            time.sleep(2)