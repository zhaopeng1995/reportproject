#!/usr/bin/python3
# encoding:utf-8


def get_monitor_info(conn):
    """
    获取监视器信息,将结果传给rfms_db_api.sync_monitor_info()
    :param conn:
    :return:
    """
    cursor = conn.cursor()
    cursor.execute('select mr.monitorkey as monitor_key,'
                   '       mr.monitorname as monitor_name,'
                   '       mr.monitortype as monitor_type,'
                   '       mr.displaytypename as monitor_type_name,'
                   '       at.name as system_name,'
                   '       a.asset_id as asset_id,'
                   '       a.NAME as server_name,'
                   '       mr.host as ip_address'
                   '  from monitor.tb_monitorrole mr'
                   '  join monitor.tb_user u '
                   '    on mr.user_id = u.user_id'
                   '  left join monitor.tb_asset a '
                   '    on mr.asset_id = a.asset_id'
                   '  left join monitor.tb_asset_type at '
                   '    on a.type_id = at.type_id'
                   ' where u.user_id = u.creator')
    data = cursor.fetchall()
    cursor.close()
    return data


def get_realtime_log(conn, begin_time=0, end_time=9999999999999):
    cursor = conn.cursor()
    # cursor.execute('select t.createtime as create_time, '
    #                '       t.monitorkey as monitor_key,'
    #                '       t.type       as monitor_type, '
    #                '       t.success    as success, '
    #                '       uncompress(t.xml) as xml'
    #                '  from monitor.tb_monitor_realtime_log_ t'
    #                ' where t.CREATETIME > %s',
    #                begin_time)
    cursor.execute('select uncompress(t.xml) as xml'
                   '  from monitor.tb_monitor_realtime_log_ t'
                   ' where t.CREATETIME between %s and %s',
                   (begin_time, end_time))
    data = cursor.fetchall()
    cursor.close()
    return data


def get_current_log_time(conn):
    cursor = conn.cursor()
    cursor.execute('select max(t.createtime), min(t.CREATETIME) max_create_time'
                   '  from monitor.tb_monitor_realtime_log_ t')
    time = cursor.fetchone()
    cursor.close()

    # print(time)  # TODO:以后改为debug日志
    if time[0] is None:
        time[0] = 0
    if time[1] is None:
        time[1] = 0
    return time
