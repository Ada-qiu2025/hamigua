# encoding: utf-8
# 调度中心的DB层,主要与数据库交互
#
import pymysql
import configparser


class MyDao:
    """主要用于数据库的操作"""

    def __init__(self, confile = 'sever.ini', ):
        """加载数据配置文件"""
        config = configparser.ConfigParser()
        config.read(confile)
        self.host = config.get('db', 'host')
        self.port = config.getint('db', 'port')
        self.user = config.get('db', 'user')
        self.passwd = config.get('db', 'passwd')

        self._conn = None
        self._cur = None

    def _connect(self, db='hospital'):
        """初始化连接及游标"""
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                    db=db)
        self.cur = self.conn.cursor()

    def get_doclist(self, _doctype=1):
        """根据type查找数据库中医生的列表,以list的形式返回"""
        li = []
        self._connect()
        self.cur.execute("select account from b_doctor where type = %d "
                         "and is_able = 0 order by account asc" % (_doctype))
        ret1 = self.cur.fetchall()
        for i in ret1:
            li.append(i[0])

        self._close()
        return li

    def get_docinfo(self, account):
        """通过医生的账号,查找医生的基本信息,并返回dict类型的信息值
        当没有找到医生的时候返回为None"""

        _docinfo = {}

        self._connect()
        self.cur.execute(
            "select account,full_name,type,sex,"
            "login_id,plat_id,plat_name,hospital_id,server_type,job_type from b_doctor where account='%s'" % (
                account))
        ret = self.cur.fetchall()

        # 将医生信息初始化
        if len(ret):
            _docinfo["account"] = ret[0][0]
            _docinfo['full_name'] = ret[0][1]

            # 1为医生,其它为药师
            if ret[0][2] == 1:
                _docinfo['type'] = 4  # 当type为1时,定义为医生
            else:
                _docinfo['type'] = ret[0][2]
            _docinfo['sex'] = ret[0][3]
            _docinfo['login_id'] = ret[0][4]
            _docinfo['plat_id'] = ret[0][5]
            _docinfo['plat_name'] = ret[0][6]
            _docinfo['hospital_id'] = ret[0][7]
            _docinfo['server_type'] = ret[0][8]
            _docinfo['job_type'] = ret[0][9]
            self._close()
            return _docinfo
        self._close()

    def get_docservice(self, account):
        """通过医生账号获取医生的服务区域,返回服务区域的list,
        医生账号不存在也会返回为[]"""
        li = []

        self._connect()
        self.cur.execute(
            "SELECT s.server_id FROM b_doctor d LEFT JOIN "
            "b_server_region_hospital s ON d.hospital_id = s.hospital_id WHERE	d.account = '%s'" % (
                account))
        ret1 = self.cur.fetchall()
        for i in ret1:
            li.append(i[0])

        self._close()
        return li

    # 根据mac地址查找药店的信息,字典的格式返回
    def get_stroreinfo(self, mac):
        _storeinfo = {}
        self._connect(db='busidb')
        self.cur.execute("SELECT s.store_id, s.chain_id, s.cn_name,"
                         "s.region_id,s.addr,s.server_id  FROM b_pc_device  d LEFT"
                         " JOIN b_store s ON s.store_id = d.store_id where d.macid = \'%s\'" % (mac))
        ret1 = self.cur.fetchall()

        # 药店信息初始化
        if len(ret1):
            _storeinfo['store_id'] = ret1[0][0]
            _storeinfo['chain_id'] = ret1[0][1]
            _storeinfo['cn_name'] = ret1[0][2]
            _storeinfo['region_id'] = ret1[0][3]
            _storeinfo['addr'] = ret1[0][4]
            _storeinfo['server_id'] = ret1[0][5]
            self._close()
            return _storeinfo
        else:
            self._close()

    def get_storelist(self):
        """根据type查找数据库中医生的列表,以list的形式返回"""
        li = []
        self._connect('busidb')
        self.cur.execute("select macid from b_pc_device order by macid asc" )
        ret1 = self.cur.fetchall()
        for i in ret1:
            li.append(i[0])

        self._close()
        return li

    def _close(self):
        """关闭数据库的连接"""
        if self.conn:
            self.conn.close()
        if self.cur:
            self.cur.close()

