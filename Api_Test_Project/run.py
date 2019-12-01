"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import unittest
import os

from datetime import datetime
# from cases import test_01_register
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import do_yaml
from scripts.handle_path import REPORTS_DIR,CONFIG_USERS_PATH,CASES_DIR
from scripts.handle_user import create_users_info

# # 创建用例套件
# suite = unittest.TestSuite()
#
# # 将模块内的所有用例加载至套件
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_01_register))
#
# # 定义一个动态时间戳的报告文件名
# result_full_path = do_yaml.read_yaml('report', 'name') + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
# # 将报告文件写入到reports文件夹
# result_full_path = os.path.join(REPORTS_DIR, result_full_path)
# # 生成测试报告
# runner = HTMLTestRunner(stream=open(result_full_path, 'wb'), title=do_yaml.read_yaml('report', 'title'), description=do_yaml.read_yaml('report', 'description'), tester=do_yaml.read_yaml('report', 'tester'))
#
# runner.run(suite)

# 判断注册用户信息yaml文件是否存在，不存在就创建，已存在则继续
if os.path.exists(os.path.join(CONFIG_USERS_PATH)) == False:
    create_users_info()

# 第一个参数为查询用例模块所在的目录路径, 第二个参数为通配符(跟shell中类似)，默认为test*
suite = unittest.defaultTestLoader.discover(CASES_DIR)

# 定义一个动态时间戳的报告文件名
result_full_path = do_yaml.read_yaml('report', 'name') + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
# 将报告文件写入到reports文件夹
result_full_path = os.path.join(REPORTS_DIR, result_full_path)
# 生成测试报告
runner = HTMLTestRunner(stream=open(result_full_path, 'wb'),
                        title=do_yaml.read_yaml('report', 'title'),
                        description=do_yaml.read_yaml('report', 'description'),
                        tester=do_yaml.read_yaml('report', 'tester'))

runner.run(suite)