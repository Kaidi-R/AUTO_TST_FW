"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import logging
import os

from scripts.handle_yaml import do_yaml
from scripts.handle_path import LOGS_DIR

class TestLog():

    @classmethod
    def create_log(cls):

        # 设置日志输出格式
        formatter = logging.Formatter(do_yaml.read_yaml('log', 'formatter'))

        # 设置日志收集器
        testlog = logging.getLogger(do_yaml.read_yaml('log', 'log_name'))
        testlog.setLevel(do_yaml.read_yaml('log', 'logger_level'))

        # 控制台处理程序
        display = logging.StreamHandler()
        display.setLevel(do_yaml.read_yaml('log', 'stream_level'))
        display.setFormatter(formatter)
        testlog.addHandler(display)

        # 输出文件处理程序
        testlog_file = logging.FileHandler(filename=os.path.join(LOGS_DIR, do_yaml.read_yaml('log', 'logfile_name')), encoding='utf8')
        testlog_file.setLevel(do_yaml.read_yaml('log', 'logfile_level'))
        testlog_file.setFormatter(formatter)
        testlog.addHandler(testlog_file)

        # 返回收集器
        return testlog

do_log = TestLog.create_log()