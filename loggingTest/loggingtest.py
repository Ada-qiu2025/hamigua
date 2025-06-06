#-*-coding:utf-8-*-
import logging
import os
from logging import config

os.chdir('E:\Pydemo\loggingTest')
config.fileConfig('logging.conf')

logging.getLogger('login').info('login-Test information')
logging.getLogger('logout').info('logout-Test information')
logging.getLogger('receive').info('receive-Test information')