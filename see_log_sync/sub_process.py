#!/usr/bin/python3
# encoding:utf-8

import time
import random

from collections import Iterable
# from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

from others import logger, timestamp_datetime
from PyMysqlPool import db
from SeeDataAnalyser import analyser
from db_api import rfms, see
from settings import *


def sync_monitor_info(log_queue):
    """
    同步see监视器信息
    :param log_queue: 存放日志信息,供日志进程使用
    :return: None
    """
    rfms_pool = db.PyMysqlPool(user='rfms', pwd='rfms', database='rfms', max_connection=1)
    see_pool = db.PyMysqlPool(user='root', pwd='tyf123', database='monitor', max_connection=1)

    while True:
        rfms_conn = rfms_pool.get_connection()
        see_conn = see_pool.get_connection()

        logger(log_queue, INFO, 'begin to sync monitor info')
        monitor_info = see.get_monitor_info(see_conn)
        rfms.sync_monitor_info(rfms_conn, monitor_info)
        logger(log_queue, INFO, 'sync monitor success')

        # 每小时同步一次
        time.sleep(poll_time)


def get_data_from_see(target_queue, log_queue):
    """
    读取see中tb_monitor_realtime_log_表的xml列,并存入target_queue队列中
    :param target_queue: 存放读取到的数据的队列,供解析进程使用
    :param log_queue: 存放日志信息,供日志进程使用
    :return: None
    """
    # global rfms_db, see_db
    logger(log_queue, INFO, 'data read process start!')
    rfms_pool = db.PyMysqlPool(user='rfms', pwd='rfms', database='rfms', max_connection=1)
    see_pool = db.PyMysqlPool(user='root', pwd='tyf123', database='monitor', max_connection=1)

    first = first_sync_all

    see_conn = see_pool.get_connection()
    max_in_see, min_in_see = see.get_current_log_time(see_conn)
    see_pool.close_connection(see_conn)

    logger(log_queue, DEBUG, 'get mxa in rfms')
    rfms_conn = rfms_pool.get_connection()
    max_in_rfms = rfms.get_current_log_time(rfms_conn)
    rfms_pool.close_connection(rfms_conn)

    begin_time = max(max_in_rfms, min_in_see)
    end_time = begin_time + sync_step

    # print(begin_time, end_time)
    while True:
        # step = 3600000
        # print(begin_time, end_time)
        try:
            rfms_conn = rfms_pool.get_connection()
            max_in_rfms = rfms.get_current_log_time(rfms_conn)
            rfms_pool.close_connection(rfms_conn)

            # print('get mxa in rfms')
            logger(log_queue, DEBUG, 'get mxa in rfms')
            see_conn = see_pool.get_connection()
            max_in_see, min_in_see = see.get_current_log_time(see_conn)
            see_pool.close_connection(see_conn)

            # print(max_in_rfms, max_in_see)
            logger(log_queue, INFO,
                   'newest log time is %s, current log time is %s' % (timestamp_datetime(max_in_see),
                                                                      timestamp_datetime(max_in_rfms))
                   )

        except Exception as e:
            logger(log_queue, ERROR, e)
            first = False
            continue

        if first:
            begin_time = max_in_rfms + 1
            end_time = max_in_see
            logger(log_queue, DEBUG,
                   'begin_time is %s, end_time is %s, ' % (timestamp_datetime(begin_time),
                                                           timestamp_datetime(end_time)))
        # elif target_queue.empty():
        else:
            # if begin_time >= end_time:
            if begin_time >= max_in_see:
                # print('no new data to get from see')
                logger(log_queue, DEBUG,
                       'begin_time is %s, end_time is %s, '
                       'no new data to get' % (timestamp_datetime(begin_time),
                                               timestamp_datetime(end_time)))

                time.sleep(read_proc_poll_time)
                first = False
                continue
            else:
                # print(end_time + sync_step, max_in_see)
                end_time = min(end_time + sync_step, max_in_see)
                logger(log_queue, DEBUG,
                       'begin_time is %s, end_time is %s, ' % (timestamp_datetime(begin_time),
                                                               timestamp_datetime(end_time)))
        # else:
        #
        #     # print('wait target_queue to empty')
        #     logger(log_queue, DEBUG, 'wait target_queue to empty')
        #     time.sleep(5)
        #     first = False
        #     continue

        # print(begin_time, end_time, max_in_see, max_in_rfms, min_in_see)
        logger(log_queue, DEBUG, (begin_time, end_time, max_in_see, max_in_rfms, min_in_see))
        try:
            see_conn = see_pool.get_connection()
            realtime_logs = see.get_realtime_log(see_conn, begin_time=begin_time, end_time=end_time)
            see_pool.close_connection(see_conn)
            # print('get realtime others : %s' % len(realtime_logs))
            logger(log_queue, INFO, 'get realtime records : %s' % len(realtime_logs))
            if realtime_logs:
                cnt = 0
                for log in realtime_logs:
                    cnt += 1
                    target_queue.put(log)
                # print('put %d record into queue' % cnt)
                logger(log_queue, DEBUG, 'put %d record into queue' % cnt)
            else:
                # print('get nothing: %s' % time.time())
                logger(log_queue, DEBUG, 'get nothing: %s' % time.time())
                first = False
                continue

            # realtime_logs = see.get_realtime_log(see_conn, begin_time=0)
        except Exception as e:
            logger(log_queue, ERROR, e)
            raise e
        first = False
        begin_time = end_time + 1
        time.sleep(read_proc_poll_time/4)


def parse_log(source_queue, target_queue, log_queue):
    """
    从source_queue读取准备解密的xml数据,并将解密完成的数据放入target_queue
    :param source_queue: 存放待解析XML数据的队列
    :param target_queue: 存放解析后XML数据的队列,供数据库插入进程使用
    :param log_queue: 存放日志信息的队列,供日志进程使用
    :return: None
    """
    logger(log_queue, INFO, 'parse process start!')
    cnt = 0
    while True:
        # print(source_queue.empty())
        logger(log_queue, DEBUG, 'is source_log_queue empty? %s' % source_queue.empty())
        if not source_queue.empty():
            log = source_queue.get(timeout=1)
            # print('%s parse_log' % log)
            # print('%s parse_log' % type(log))

            xml = analyser.decode_xml(log[0])
            # print(xml)
            dict_xml = analyser.analyse_xml(xml)

            target_queue.put((dict_xml, xml), timeout=1)
            cnt += 1
            # print('#######parse_data######')
            logger(log_queue, DEBUG, 'decode_log_queue size is: %s' % target_queue.qsize())
            # print(decode_log_queue.qsize(), type(decode_log_queue.qsize()))
            # print('decode_log_queue size is: %s' % decode_log_queue.qsize())
            # break

        else:
            # print('%s has been parse.Nothing to parse: %s' % (cnt, time.time()))
            logger(log_queue, DEBUG, '%s has been parse.Nothing to parse: %s' % (cnt, time.time()))
            time.sleep(parse_proc_poll_time)
            continue
    print('end')


def insert_log_to_db(source_queue, log_queue):
    """
    从source_target读取待插入的数据,并插入到数据库中对应的记录表
    :param source_queue: 存放着待插入到数据库的信息
    :param log_queue: 存放日志信息,供日志进程使用
    :return:
    """
    logger(log_queue, INFO, 'data write process start!')
    rfms_pool = db.PyMysqlPool(user='rfms', pwd='rfms', database='rfms', max_connection=2)
    cnt = 0
    while True:
        # print('source_queue is empty : %s' % source_queue.empty())
        logger(log_queue, DEBUG, 'source_queue is empty : %s' % source_queue.empty())

        if source_queue.empty():
            # print('%s has been insert, no data to insert %s' % (cnt, time.time()))
            logger(log_queue, DEBUG, '%s has been insert, no data to insert %s' % (cnt, time.time()))
            time.sleep(write_proc_poll_time)
            continue
        # print('get_source_queue')
        record = source_queue.get_nowait()
        create_time = record[0]['create_time']
        monitor_key = record[0]['monitor_key']
        monitor_type = record[0]['monitor_type']
        success = record[0]['success']

        # 记录原始记录
        # print('get realtime connection start')
        rfms_conn = rfms_pool.get_connection()
        # print('get realtime conncetion success')
        try:
            # print('insert realtime log start')
            rfms.monitor_realtime_log(rfms_conn, create_time, monitor_key, monitor_type, success, record[1])
            # rfms_conn.commit()
            # print('insert realtime log end')
            cnt += 1
        except Exception as e:
            logger(log_queue, ERROR, e)
            # raise e
        finally:
            # print('close realtime connection')
            rfms_pool.close_connection(rfms_conn)
            # print('close realtime connection finish')

        for key, item in record[0].items():
            if hasattr(rfms.InsertLog, key):

                # print('get item connection start')
                rfms_conn = rfms_pool.get_connection()
                # print('get item conncetion success')
                try:
                    # print('insert %s log start' % key)
                    getattr(rfms.InsertLog, key)(rfms_conn, create_time, monitor_key, item)
                    rfms_conn.commit()
                    # print('insert %s log end' % key)
                except Exception as e:
                    print(e)
                    raise e
                finally:

                    # print('close item connection')
                    rfms_pool.close_connection(rfms_conn)
                    # print('close item connection finish')
                    # print('########insert data#########', )
            else:
                pass


def log_process(log_queue):
    """
    日志进程,统一写日志,避免不必要的IO竞争
    :param log_queue: 日志队列
    :return: None
    """

    import os
    import sys
    import logging

    from logging.handlers import TimedRotatingFileHandler

    level_ = {CRITICAL: 'CRITICAL', ERROR: 'ERROR', WARNING: 'WARNING', INFO: 'INFO', DEBUG: 'DEBUG'}

    path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    log_path = os.path.join(path, 'logs')
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    # 初始化logging
    file_name = os.path.join(path, 'logs', 'data_sync.log')

    fh = TimedRotatingFileHandler(filename=file_name, when='midnight')
    ch = logging.StreamHandler()
    fmt = logging.Formatter('%(message)s')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    main_logger = logging.getLogger('log')
    main_logger.setLevel(log_level)
    main_logger.addHandler(fh)
    main_logger.addHandler(ch)

    while True:
        if log_queue.empty():

            time.sleep(random.random())
        else:
            log = log_queue.get()

            t, level, message = log
            if isinstance(message, Iterable) and not isinstance(message, str):
                message = ', '.join([str(i) for i in message])
            main_logger.debug(' '.join([t, '-', level_[level], '-', message]))

            if level == DEBUG:
                main_logger.debug(' '.join([t, '-', level_[level], '-', message]))
            elif level == INFO:
                main_logger.info(' '.join([t, '-', level_[level], '-', message]))
            elif level == WARNING:
                main_logger.warning(' '.join([t, '-', level_[level], '-', message]))
            elif level == ERROR:
                main_logger.error(' '.join([t, '-', level_[level], '-', message]))
            elif level == CRITICAL:
                main_logger.critical(' '.join([t, '-', level_[level], '-', message]))
            else:
                main_logger.debug(' '.join([t, '-', level_[level], '-', message]))
