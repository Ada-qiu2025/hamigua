# encoding: utf-8

from mypackage.disPacher import *
import time
import logging.config
import mypackage.stateCenter as SC
import logging.handlers
import unittest
from mypackage.D_other import *

# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
mylogger = logging.getLogger('root')



