#!/usr/bin/python3
# encoding:utf-8
import gzip
import base64
from xml.etree import ElementTree
from SeeDataAnalyser.recordsetanalyser import RecordSetAnalyser


def decode_xml(encode_data):
    """
    解码xml文件
    :param encode_data: 输入加密的xml信息
    :return: 解密的xml内容
    """
    zip_data = base64.b64decode(encode_data)
    data = gzip.decompress(zip_data).decode()
    return data


def analyse_xml(data):
    log = dict()
    root = ElementTree.fromstring(data)
    create_time = int(root.find('createtime').text)
    monitor_key = root.find('monitorKey').text
    monitor_type = root.find('monitorType').text
    success = root.find('success').text

    log['create_time'] = create_time
    log['monitor_key'] = monitor_key
    log['monitor_type'] = monitor_type
    log['success'] = success

    for record_set in root.iter('recordset'):
        record_type = record_set.get('name').lower()
        func_name = monitor_type.lower() + '_' + record_type
        try:
            records = getattr(RecordSetAnalyser, func_name)(record_set)
        except Exception as e:
            print(e)
            raise e
        if records:
            log[func_name] = records
    return log
