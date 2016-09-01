#!/usr/bin/python3
# encoding:utf-8
from SeeDataAnalyser.dicts import *


def nvl(value, null_value):
    if value is None:
        return null_value
    else:
        return value


def _to0(value, _value):
    if value == '-':
        return _value
    else:
        return value


class RecordSetAnalyser(object):
    def __getattr__(self, attr):
        return ['%s has no analyser' % attr]

    # linux
    @staticmethod
    def lagentlinux_cpu(record_set):
        cpu_record = list()
        for record in record_set:
            cpu = float(record.find('CpuUsage').text)
            cpu_record.append((cpu,))
        return cpu_record

    @staticmethod
    def lagentlinux_memory(record_set):
        memory_record = list()
        for record in record_set:
            total_phys = float(record.find('TotalPhys').text)
            avail_phys = float(record.find('AvailPhys').text)
            used_phys = float(record.find('UsedPhys').text)
            total_page_file = float(record.find('TotalPageFile').text)
            avail_page_file = float(record.find('AvailPageFile').text)
            used_page_file = float(record.find('UsedPageFile').text)
            memory_used_rate = float(record.find('MemoryUsedRate').text)
            memory_load = float(record.find('MemoryLoad').text)
            page_file_used_rate = float(record.find('pageFileUsedRate').text)
            memory_record.append((total_phys, avail_phys, used_phys, total_page_file, avail_page_file, used_page_file,
                                  memory_used_rate, memory_load, page_file_used_rate))
        return memory_record

    @staticmethod
    def lagentlinux_storage(record_set):
        storage_record = list()
        for record in record_set:
            drive = record.find('Drive').text
            total_bytes = float(record.find('TotalBytes').text)
            total_free_bytes = float(record.find('TotalFreeBytes').text)
            free_bytes_available = float(record.find('FreeBytesAvailable').text)
            drive_type = record.find('DriveType').text
            hit_info = record.find('HitInfo').text
            used_rate = float(record.find('UsedRate').text)
            storage_record.append((drive, total_bytes, total_free_bytes, free_bytes_available, drive_type, hit_info,
                                   used_rate))
        return storage_record

    # win
    lagentwin_cpu = lagentlinux_cpu

    lagentwin_memory = lagentlinux_memory

    lagentwin_storage = lagentlinux_storage

    @staticmethod
    def lagentwin_agenterror(record_set):
        agent_error_record = list()
        for record in record_set:
            error_info = record.find('errorInfo').text
            function_id = int(record.find('functionID').text)
            agent_error_record.append((error_info, function_id))
        return agent_error_record

    # ar
    @staticmethod
    def ar_speed(record_set):
        speed_record = list()
        for record in record_set:
            recv_packets = int(record.find('recvPackets').text)
            sent_packets = int(record.find('sentPackets').text)
            recv_packets_per_sec = int(record.find('recvPacketsPerSec').text)
            sent_packets_per_sec = int(record.find('sentPacketsPerSec').text)
            speed_record.append((recv_packets, sent_packets, recv_packets_per_sec, sent_packets_per_sec))
        return speed_record

    @staticmethod
    def ar_session(record_set):
        session_record = list()
        for record in record_set:
            session_id = int(record.find('sessionId').text)
            session_name = record.find('sessionName').text
            session_type = record.find('sessionType').text
            recv_packets = int(record.find('recvPackets').text)
            sent_packets = int(record.find('sentPackets').text)
            recv_packets_per_sec = int(record.find('recvPacketsPerSec').text)
            sent_packets_per_sec = int(record.find('sentPacketsPerSec').text)
            session_record.append((session_id, session_name, session_type, recv_packets, sent_packets,
                                   recv_packets_per_sec, sent_packets_per_sec))
        return session_record

    # as
    @staticmethod
    def as_waitrequests(record_set):
        wait_requests_record = list()
        for record in record_set:
            no = record.find('no').text
            business_type = record.find('business_type').text
            priority = record.find('priority').text
            data_node = record.find('data_node').text
            empty_node = record.find('empty_node').text
            wait_requests_record.append((no, business_type, priority, data_node, empty_node))
        return wait_requests_record

    @staticmethod
    def as_datasource(record_set):
        data_source_record = list()
        for record in record_set:
            logic_name = record.find('LogicName').text
            db_driver_type = record.find('DBDriverType').text
            server_name = record.find('ServerName').text
            user_name = record.find('UserName').text
            init_connection_count = int(record.find('InitConnectionCount').text)
            real_connection_count = int(record.find('RealConnectionCount').text)
            busy_connection_count = int(record.find('BusyConnectionCount').text)
            free_connection_count = int(record.find('FreeConnectionCount').text)
            max_busy_connection_count = int(record.find('MaxBusyConnectionCount').text)
            disconnect_count = int(record.find('DisconnectionCount').text)
            is_temp_data_source = record.find('IsTempDataSource').text
            available = bool_dict[record.find('Available').text.lower()]
            data_source_record.append((logic_name, db_driver_type, server_name, user_name,
                                       init_connection_count, real_connection_count, busy_connection_count,
                                       free_connection_count, max_busy_connection_count, disconnect_count,
                                       is_temp_data_source, available))
        return data_source_record

    @staticmethod
    def as_memorydb(record_set):
        memory_db_record = list()
        for record in record_set:
            table_name = record.find('tableName').text
            record_count = int(record.find('recordCount').text)
            status = record.find('status').text
            data_source = record.find('dataSource').text
            data_source_table_name = record.find('dataSourceTableName').text
            data_source_sql = record.find('dataSourceSQL').text
            data_source_cache = record.find('dataSourceCache').text
            memory_db_record.append((table_name, record_count, status, data_source, data_source_table_name,
                                     data_source_sql, data_source_cache))
        return memory_db_record

    @staticmethod
    def as_sysarg(record_set):
        pass

    @staticmethod
    def as_threadtimeout(record_set):
        thread_timeout_record = list()
        for record in record_set:
            thread_id = int(record.find('thread_id').text)
            status = int(record.find('status').text)
            request_num = int(record.find('request_num').text)
            answer_num = int(record.find('answer_num').text)
            function_no = int(record.find('function_no').text)
            thread_timeout_record.append((thread_id, status, request_num, answer_num, function_no))
        return thread_timeout_record

    @staticmethod
    def as_session(record_set):
        session_record = list()
        for record in record_set:
            session_id = int(record.find('sessionId').text)
            session_name = record.find('sessionName').text
            session_type = record.find('sessionType').text
            recv_packets = int(record.find('recvPackets').text)
            sent_packets = int(record.find('sentPackets').text)
            recv_packets_per_sec = int(record.find('recvPacketsPerSec').text)
            sent_packets_per_sec = int(record.find('sentPacketsPerSec').text)
            session_record.append((session_id, session_name, session_type, recv_packets, sent_packets,
                                   recv_packets_per_sec, sent_packets_per_sec))
        return session_record

    # esb监视器
    @staticmethod
    def esb_route_queue(record_set):
        route_queue_record = list()
        for record in record_set:
            msg_in_queue = record.find('MsgInQ').text
            max_msg_in_queue = record.find('MaxMsgInQ').text
            if_self_pause = record.find('IFSelfPause').text
            route_queue_record.append((msg_in_queue, max_msg_in_queue, if_self_pause))
        return route_queue_record

    @staticmethod
    def esb_route_table(record_set):
        route_table_record = list()
        for record in record_set:
            route_item_no = int(record.find('RouterItemNo').text)
            if_enable = record.find('IfEnable').text
            truncation = record.find('truncation').text
            system_no = record.find('system_no').text
            sub_system_no = record.find('sub_system_no').text
            function_id = record.find('functionid').text
            branch_no = record.find('branchno').text
            node_name = record.find('nodename').text
            svr_name = record.find('svrname').text
            plugin_id = record.find('pluginid').text
            need_ospf = record.find('needospf').text
            forbinden = record.find('forbiden').text
            status = record.find('status').text
            route_table_record.append((route_item_no, if_enable, truncation, system_no, sub_system_no, function_id,
                                       branch_no, node_name, svr_name, plugin_id, need_ospf, forbinden, status))

    @staticmethod
    def esb_f1_queue(record_set):
        f1_queue_record = list()
        for record in record_set:
            msg_in_queue = int(record.find('MsgInQ').text)
            max_msg_in_queue = int(record.find('MaxMsgInQ').text)
            f1_queue_record.append((msg_in_queue, max_msg_in_queue))
        return f1_queue_record

    @staticmethod
    def esb_f2_queue(record_set):
        f2_queue_record = list()
        for record in record_set:
            msg_in_queue = int(record.find('MsgInQ').text)
            max_msg_in_queue = int(record.find('MaxMsgInQ').text)
            f2_queue_record.append((msg_in_queue, max_msg_in_queue))
        return f2_queue_record

    @staticmethod
    def esb_f2_conn_count(record_set):
        f2_conn_count_record = list()
        for record in record_set:
            named_count = int(record.find('named_count').text)
            f2_conn_count_record.append((named_count, ))
        return f2_conn_count_record

    @staticmethod
    def esb_f2_rucp_cnt(record_set):
        f2_rucp_cnt_record = list()
        for record in record_set:
            local_id = record.find('LocalID').text
            peer_id = int(record.find('PeerID').text)
            status = record.find('Status').text
            address = record.find('Address').text
            retransfer_nodes = int(record.find('ReTransferNodes').text)
            stat_max_retry_times = int(record.find('StatMaxRetryTimes').text)
            retry_send_pieces = int(record.find('RetrySendPieces').text)
            if record.find('RetrySendPiecesPsc') is None:
                retry_send_pieces_per_sec = 0
            else:
                retry_send_pieces_per_sec = int(record.find('RetrySendPiecesPsc').text)
            f2_rucp_cnt_record.append((local_id, peer_id, status, address, retransfer_nodes,
                                       stat_max_retry_times, retry_send_pieces, retry_send_pieces_per_sec))
        return f2_rucp_cnt_record

    @staticmethod
    def esb_esbmessagefacotry_info(record_set):
        esbmessagefacotry_info_record = list()
        for record in record_set:
            current_total_msgs = int(record.find('CurrentTotalMsgs').text)
            current_idle_msgs_in_pool = int(record.find('CurrentIdleMsgsInPool').text)
            run_time_max_total_msgs = int(record.find('RunTimeMaxTotalMsgs').text)
            max_total_msgs = int(record.find('MaxTotalMsgs').text)
            max_idle_msg_in_pool = int(record.find('MaxIdleMsgsInPool').text)
            msg_pool_size = int(record.find('MsgPoolSize').text)
            esbmessagefacotry_info_record.append((current_total_msgs, current_idle_msgs_in_pool,
                                                  run_time_max_total_msgs, max_total_msgs, max_idle_msg_in_pool,
                                                  msg_pool_size))
        return esbmessagefacotry_info_record

    @staticmethod
    def esb_t2_conn_count(record_set):
        t2_conn_count_record = list()
        for record in record_set:
            named_count = int(record.find('named_count').text)
            connection_count = int(record.find('connection_count').text)
            t2_conn_count_record.append((named_count, connection_count))

    @staticmethod
    def esb_t2_config_info(record_set):
        t2_config_info_record = list()
        for record in record_set:
            safe_level = record.find('safe_level').text
            protocol = record.find('protocol').text
            address = record.find('address').text
            port = int(record.find('port').text)
            thread_count = int(record.find('thread_count').text)
            max_connection = int(record.find('max_connection').text)
            init_connection = int(record.find('init_connection').text)
            init_recv_buf_size = int(record.find('init_recv_buf_size').text)
            init_send_buf_size = int(record.find('init_send_buf_size').text)
            send_queue_size = int(record.find('send_queue_size').text)
            register_time = int(record.find('register_time').text)
            heartbeat_time = int(record.find('heartbeat_time').text)
            accept_count = int(record.find('accept_count').text)
            send_count = int(record.find('send_count').text)
            recv_count = int(record.find('recv_count').text)
            plugin_name = record.find('plugin_name').text
            t2_config_info_record.append((safe_level, protocol, address, port, thread_count, max_connection,
                                          init_connection, init_recv_buf_size, init_send_buf_size, send_queue_size,
                                          register_time, heartbeat_time, accept_count, send_count, recv_count,
                                          plugin_name))
        return t2_config_info_record

    @staticmethod
    def esb_speed(record_set):
        speed_record = list()
        for record in record_set:
            transfer_packets = int(record.find('TransferPackets').text)
            cant_transfer_packets = int(record.find('CantTransferPackets').text)
            transfer_packet_per_sec = int(record.find('TransferPacketsPerSec').text)
            speed_record.append((transfer_packets, cant_transfer_packets, transfer_packet_per_sec))
        return speed_record

    @staticmethod
    def esb_summarydata(record_set):
        """
        esb summaryData
        :param record_set:
        :return:
        """
        summary_data_record = list()
        for record in record_set:
            transfer_packets_per_sec = record.find('TransferPacketsPerSec').text
            t2_conn_count = int(nvl(record.find('t2_conn_count').text, 0))
            msg_fac_info = record.find('msgFac_info').text
            f2_conn_count = int(nvl(record.find('f2_conn_count').text, 0))
            if_self_pause = record.find('IFSelfPause').text
            hsdb_conn_cfg = record.find('hsdb_conn_cfg').text
            summary_data_record.append((transfer_packets_per_sec, t2_conn_count, msg_fac_info, f2_conn_count,
                                       if_self_pause, hsdb_conn_cfg))
        return summary_data_record

    @staticmethod
    def esb_procbizfunclibs(record_set):
        """
        esb ProcBizFuncLibs
        :param record_set:
        :return:
        """
        pass

    @staticmethod
    def esb_proc_queue(record_set):
        pass

    @staticmethod
    def esb_proc_pool_info(record_set):
        pass

    @staticmethod
    def esb_hsdb_conn_cfg(record_set):
        hsdb_conn_cfg_record = list()
        for record in record_set:
            logic_name = record.find('LogicName').text
            real_connection_count = int(record.find('RealConnectionCount').text)
            free_connection_count = int(record.find('FreeConnectionCount').text)
            disconnection_count = int(record.find('DisconnectionCount').text)
            busy_connection_count = int(record.find('BusyConnectionCount').text)
            wait_user_count = int(record.find('WaitUserCount').text)
            hsdb_conn_cfg_record.append((logic_name, real_connection_count, free_connection_count, disconnection_count,
                                         busy_connection_count, wait_user_count))
        return hsdb_conn_cfg_record

    @staticmethod
    def esb_warn_mdb_table_disable(record_set):
        pass

    @staticmethod
    def esb_sysarg(record_set):
        sys_arg_record = list()
        for record in record_set:
            company_no = int(record.find('company_no').text)
            company_name = record.find('company_name').text
            user_id = int(record.find('user_id').text)
            branch_no = int(record.find('branch_no').text)
            branch_name = record.find('branch_name').text
            init_date = int(record.find('init_date').text)
            sys_status = int(record.find('sys_status').text)
            system_name = record.find('system_name').text
            sys_arg_record.append((company_no, company_name, user_id, branch_no, branch_name, init_date, sys_status,
                                   system_name))
        return sys_arg_record

    # lAgentExpandLog
    @staticmethod
    def lagentexpandlog_agenterror(record_set):
        pass

    @staticmethod
    def lagentexpandlog_mf_getuniversallogex(record_set):
        pass

    # lAgentLog
    @staticmethod
    def lagentlog_warning(record_set):
        pass

    # lAgentOracle
    @staticmethod
    def lagentoracle_hits_ratio(record_set):
        hits_ratio_record = list()
        for record in record_set:
            buffer_hits = float(record.find('buffer_hits').text)
            lib_hits = float(record.find('libhits').text)
            dd_hits = float(record.find('ddhits').text)
            hits_ratio_record.append((buffer_hits, lib_hits, dd_hits))
        return hits_ratio_record

    @staticmethod
    def lagentoracle_connanduser(record_set):
        """
        lAgentOracle connAndUser
        :param record_set:
        :return:
        """
        conn_and_user_record = list()
        for record in record_set:
            connect_num = int(record.find('connect_num').text)
            active_user = int(record.find('active_user').text)
            conn_and_user_record.append((connect_num, active_user))
        return conn_and_user_record

    @staticmethod
    def lagentoracle_tablespacestat(record_set):
        """
        lAgentOracle tablespaceStat
        :param record_set:
        :return:
        """
        tablespace_stat_record = list()
        for record in record_set:
            tablespace_name = record.find('tablespace_name').text
            total_space = float(record.find('total_space').text)
            used_space = float(record.find('used_space').text)
            free_pct = float(record.find('free_pct').text)
            free_space = float(record.find('free_space').text)
            online_status = record.find('online_status').text
            count = int(record.find('count').text)
            contents = record.find('contents').text
            extent_management = record.find('extent_management').text
            segment_space_management = record.find('segment_space_management').text
            tablespace_stat_record.append((tablespace_name, total_space, used_space, free_pct, free_space,
                                           online_status, count, contents, extent_management, segment_space_management))
        return tablespace_stat_record

    @staticmethod
    def lagentoracle_dbdesc(record_set):
        """
        lAgentOracle dbDesc
        :param record_set:
        :return:
        """
        db_desc_record = list()
        for record in record_set:
            name = record.find('name').text
            created = record.find('created').text
            log_mode = record.find('log_mode').text
            controlfile_type = record.find('controlfile_type').text
            open_mode = record.find('open_mode').text
            protection_mode = record.find('protection_mode').text
            protection_level = record.find('protection_level').text
            database_role = record.find('database_role').text
            switchover_status = record.find('switchover_status').text
            guard_status = record.find('guard_status').text
            db_desc_record.append((name, created, log_mode, controlfile_type, open_mode, protection_mode,
                                   protection_level, database_role, switchover_status, guard_status))
        return db_desc_record

    @staticmethod
    def lagentoracle_mf_getdlsession(record_set):
        pass

    @staticmethod
    def lagentoracle_sgastat(record_set):
        sga_stat_record = list()
        for record in record_set:
            name = record.find('name').text
            size = int(record.find('bytes').text)
            sga_stat_record.append((name, size))
        return sga_stat_record

    @staticmethod
    def lagentoracle_lockstat(record_set):
        lock_stat_record = list()
        for record in record_set:
            lock_type = record.find('type').text
            count = int(record.find('count').text)
            lock_stat_record.append((lock_type, count))
        return lock_stat_record

    @staticmethod
    def lagentoracle_lockobject(record_set):
        # TODO: 以后需要添加这个信息
        pass

    # lAgentPing TODO: 以后添加lAgentPing监视器解析
    @staticmethod
    def lagentping_pingstat(record_set):
        # lAgentPing pingstat
        ping_stat_record = list()
        for record in record_set:
            host_name = record.find('HostName').text
            host_ip = record.find('HostIP').text
            sent = record.find('Sent').text
            received = record.find('Received').text
            loss_rate = record.find('LossRate').text
            avg_time = record.find('AvgTime').text
            ttl = record.find('TTL').text
            ping_stat_record.append((host_name, host_ip, sent, received, loss_rate, avg_time, ttl))
        return ping_stat_record

    # lAgentPort TODO: 以后添加lAgentPort监视器解析

    # mysql TODO:以后添加mysql监视器解析

    # process_lAgent
    @staticmethod
    def process_lagent_process(record_set):
        process_record = list()
        for record in record_set:

            user = record.find('User').text
            command = record.find('Command').text
            read_operation_count = int(_to0(record.find('read_operation_count').text, 0))
            write_operation_count = int(_to0(record.find('write_operation_count').text, 0))
            write_transfer_count_rate = int(_to0(record.find('write_transfer_count_rate').text, 0))
            pid = int(record.find('PID').text)
            cpu_ratio = float(record.find('CpuRatio').text)
            write_operation_count_rate = int(_to0(record.find('write_operation_count_rate').text, 0))
            read_operation_count_rate = int(_to0(record.find('read_operation_count_rate').text, 0))
            mem_ratio = float(record.find('MemRatio').text)
            original_phys_mem = int(record.find('OriginalPhysMem').text)
            status = record.find('Statu').text
            original_vir_mem = int(record.find('OriginalVirMem').text)
            name = record.find('Name').text
            stime = record.find('Stime').text
            write_transfer_count = int(_to0(record.find('write_transfer_count').text, 0))
            read_transfer_count = int(_to0(record.find('read_transfer_count').text, 0))
            virtual_mem = int(record.find('VirtualMem').text)
            physical_mem = int(record.find('PhysicalMem').text)
            read_transfer_count_rate = record.find('read_transfer_count_rate').text
            vir_mem_grow_ratio = float(record.find('VirMemGrowRatio').text)
            phys_mem_grow_ratio = float(record.find('PhysMemGrowRatio').text)
            process_record.append((read_operation_count, command, user, write_operation_count,
                                   write_transfer_count_rate, pid, cpu_ratio, write_operation_count_rate,
                                   read_operation_count_rate, mem_ratio, original_phys_mem, status,
                                   original_vir_mem, name, stime, write_transfer_count, read_transfer_count,
                                   virtual_mem, physical_mem, read_transfer_count_rate, vir_mem_grow_ratio,
                                   phys_mem_grow_ratio))
        return process_record

    @staticmethod
    def process_lagent_processstat(record_set):
        process_stat_record = list()
        for record in record_set:
            name = record.find('Name').text
            process_count = int(record.find('ProcessCount').text)
            process_stat_record.append((name, process_count))
        return process_stat_record

    # tcpcon_snmp
    @staticmethod
    def tcpcon_snmp_netstat(record_set):
        net_stat = list()
        for record in record_set:
            tcp_conn_local_address = record.find('tcpConnLocalAddress').text
            tcp_conn_local_port = int(record.find('tcpConnLocalPort').text)
            tcp_conn_rem_address = record.find('tcpConnRemAddress').text
            tcp_conn_rem_port = int(record.find('tcpConnRemPort').text)
            tcp_conn_state = record.find('tcpConnState').text
            net_stat.append((tcp_conn_local_address, tcp_conn_local_port, tcp_conn_rem_address, tcp_conn_rem_port,
                             tcp_conn_state))
        return net_stat

    @staticmethod
    def tcpcon_snmp_countstat(record_set):
        count_stat = list()
        for record in record_set:
            count = int(record.find('count').text)
            count_stat.append((count, ))
        return count_stat
