#!/usr/bin/python3
# encoding:utf-8


def sync_monitor_info(conn, data):
    """
    同步监视器信息
    :param conn: 链接rfms数据库
    :param data: 从see数据库读取的数据,见see_db_api.get_monitor_info()
    :return: error_code
    """
    cursor = conn.cursor()
    cursor.execute('select monitor_key'
                   '  from rfms.monitor_info')

    monitor_keys = cursor.fetchall()
    monitors = [item[0] for item in monitor_keys]
    need_update = list()
    for record in data:
        if record[0] not in monitors:
            need_update.append(record[0])
            cursor.execute('insert into rfms.monitor_info '
                           'values(%s, %s, %s, %s, %s, %s, %s, %s)',
                           record)
    # conn.commit()
    cursor.close()
    return 0


def get_current_log_time(conn):
    cursor = conn.cursor()
    cursor.execute('select max(t.create_time) max_create_time'
                   '  from rfms.monitor_realtime_log t')
    date = cursor.fetchone()
    cursor.close()

    # print(date)  # TODO:以后改为debug日志
    if date[0] is None:
        return 0
    return date[0]


def monitor_realtime_log(conn, create_time, monitor_key, monitor_type, success, xml):
    cursor = conn.cursor()
    cursor.execute('insert into rfms.monitor_realtime_log(create_time, monitor_key, monitor_type, success, xml) '
                   'values(%s, %s, %s, %s, %s)',
                   (create_time, monitor_key, monitor_type, success, xml))
    return 0


class InsertLog(object):
    # 插入数据的部分
    def __getattr__(self, attr):
        return '%s did not way to insert into rfms db' % attr

    @staticmethod
    def lagentlinux_cpu(conn, create_time, monitor_key, records):
        cursor = conn.cursor()
        for record in records:
            args = [create_time, monitor_key]
            args.extend(record)
            # print(args)
            try:
                cursor.execute('insert into rfms.cpu_log(create_time, monitor_key, cpu_usage) '
                               'values(%s, %s, %s)',
                               args
                               )
            except Exception as e:
                print(e)
                raise e
        return 0

    lagentwin_cpu = lagentlinux_cpu

    @staticmethod
    def lagentlinux_memory(conn, create_time, monitor_key, records):
        cursor = conn.cursor()
        for record in records:
            args = [create_time, monitor_key]
            args.extend(record)
            # print(args)
            try:
                cursor.execute('insert into rfms.memory_log(create_time, monitor_key, total_phys, avail_phys, used_phys, '
                               '                            total_page_file, avail_page_file, used_page_file, '
                               '                            memory_used_rate, memory_load, page_file_used_rate) '
                               'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               args
                               )
            except Exception as e:
                print(e)
                raise e
        return 0

    lagentwin_memory = lagentlinux_memory

    @staticmethod
    def lagentlinux_storage(conn, create_time, monitor_key, records):
        cursor = conn.cursor()
        for record in records:
            args = [create_time, monitor_key]
            args.extend(record)
            try:
                cursor.execute('insert into rfms.storage_log(create_time, monitor_key, drive, total_bytes, '
                               '                             total_free_bytes, free_bytes_available, drive_type, '
                               '                             hit_info, used_rate) '
                               'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                               args)
            except Exception as e:
                print(e)
                raise e
        return 0

    lagentwin_storage = lagentlinux_storage
