#!/usr/bin/python3
# encoding:utf-8
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG


poll_time = 3600
log_level = INFO

sync_step = 3600000
first_sync_all = False

read_proc_poll_time = 60
parse_proc_poll_time = 30
write_proc_poll_time = 5