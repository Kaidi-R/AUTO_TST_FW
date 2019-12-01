"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import os

# 本文件路径，包括文件名
os.path.abspath(__file__)

# 本文件父目录路径
os.path.dirname(os.path.abspath(__file__))

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取测试用例文件夹所在路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')

# 获取配置文件所在目录路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 获取测试用例类配置文件所在路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'test_cases.yaml')

# 获取用户信息配置文件所在路径
CONFIG_USERS_PATH = os.path.join(CONFIGS_DIR, 'users_info.yaml')

# 获取日志文件所在目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告文件所在目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取excel文件所在目录路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')