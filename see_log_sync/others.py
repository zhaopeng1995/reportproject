#!/usr/bin/python3
# encoding:utf-8
from time import strftime, localtime


def logger(queue, level, message):
    t = strftime('%Y-%m-%d %H:%M:%S')
    # put a tuple
    queue.put((t, level, message))


def timestamp_datetime(value):
    datetime = strftime('%Y-%m-%d %H:%M:%S', localtime(value / 1000))
    return datetime
