#!/usr/bin/python3
# encoding:utf-8

import pymysql

from PyMysqlPool.error import *


class PyMysqlPool(object):
    def __init__(self, user, pwd, host='127.0.0.1', port=3306, database='mysql', max_connection=50, ):
        """
        初始化连接池
        :param user: 连接mysql用户名
        :param pwd: 连接mysql密码
        :param host: IP地址,默认为127.0.0.1
        :param port: 端口,默认为3306
        :param database: 指定数据库名,默认mysql
        :param max_connection: 连接池最大连接数
        """
        from queue import Queue
        self._pool = Queue(max_connection)
        # from multiprocessing import Manager
        # self.manager = Manager()
        # self._pool = self.manager.Queue(max_connection)

        self.db_info = (user, pwd, host, port, database)
        self.max_connection = max_connection

        try:
            self.fill_connection()
        except Exception as e:
            # error = '初始化失败(%s, %s)' % e.args
            # print('初始化失败' + e.args)
            print(e)
            raise e
        # print('%s init done' % database)

    def fill_connection(self):
        """
        填充数据库连接到队列
        :return:
        """
        try:
            if self._pool.qsize() < self.max_connection:
                for _ in range(self.max_connection - self._pool.qsize()):
                    self._pool.put(self.create_connection())
        except pymysql.MySQLError as e:
            print(e)
            raise e

    def get_connection(self):
        """
        获取一个数据库连接
        :return: 返回一个数据库连接
        """
        # print('%s has %d connections left' % (self.db_info[4], self._pool.qsize()))
        # print('begin to get conn')
        conn = self._pool.get(timeout=1)
        # print('begin to ping')
        # 返回连接之前先尝试重连一下
        # TODO:可能以后需要改造,用于当ping发现无效时重新获取一个连接
        try:
            # print('ping start')
        #   conn.ping(reconnect = True)
            conn.ping(reconnect = False)
            # print('ping end')
        except Exception as e:
            print('exception conn')
            del conn
            conn = self.create_connection()

        # print('return conn')
        # print('get_connect:%s' % self.db_info[4])
        return conn

    def create_connection(self):
        """
        创建一个数据库连接
        :return: None
        """
        try:
            conn = pymysql.connect(user=self.db_info[0], passwd=self.db_info[1],
                                   host=self.db_info[2], port=self.db_info[3],
                                   database=self.db_info[4],
                                   charset='utf8',
                                   connect_timeout=3,
                                   autocommit=True)
            return conn
        except pymysql.MySQLError as e:
            if e.args[0] == TOO_MANY_CONNECTIONS:
                print(e)
            else:
                print(e)
                raise e

    def close_connection(self, conn):
        """
        当连接需要关闭时调用这个方法,用于把数据库连接重新放回队列中,供下次使用
        :param conn: 需要"关闭"的连接
        :return: None
        """
        self._pool.put(conn)
        # print('close_connect:%s' % self.db_info[4])
