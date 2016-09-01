#!/usr/bin/python3
# encoding:utf-8
from multiprocessing import Pool, Process, Manager, cpu_count

from sub_process import get_data_from_see, parse_log, insert_log_to_db, sync_monitor_info, log_process


def main():

    if cpu_count() - 4 <= 0:
        # 至少给插入进程一个进程大小的进程池
        write_pool_size = 2
    else:
        write_pool_size = divmod(cpu_count() - 4, 2)[0]

    manager = Manager()
    source_log_queue = manager.Queue()
    decode_log_queue = manager.Queue()
    log_queue = manager.Queue()

    p_sync_monitor_info = Process(target=sync_monitor_info, args=(log_queue, ))
    p_get_data = Process(target=get_data_from_see, args=(source_log_queue, log_queue))
    p_parse_data = Process(target=parse_log, args=(source_log_queue, decode_log_queue, log_queue))
    p_log = Process(target=log_process, args=(log_queue, ))

    p_sync_monitor_info.daemon = True
    p_get_data.daemon = True
    p_parse_data.daemon = True
    p_log.daemon = True

    p_sync_monitor_info.start()
    p_get_data.start()
    p_parse_data.start()
    p_log.start()

    write_pool = Pool(write_pool_size)

    # 塞满进程池
    for _ in range(write_pool_size):
        write_pool.apply_async(insert_log_to_db, args=(decode_log_queue, log_queue))

    p_sync_monitor_info.join()
    p_get_data.join()
    p_parse_data.join()
    p_log.join()

    write_pool.close()
    write_pool.join()


if __name__ == '__main__':
    main()