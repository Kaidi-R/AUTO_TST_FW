"""
===========================
Author:帅迪
Time:2019/11/6
Mail:1306177347qq.com
===========================
"""

import yaml

from scripts.handle_path import CONFIG_FILE_PATH

class HandleYaml():

    # 初始化
    def __init__(self, filename):
        with open(filename, encoding='utf-8') as file:
            self.datas = yaml.full_load(file)
    # 读取数据
    def read_yaml(self, section, option):
        return self.datas[section][option]

    # 写入数据
    @staticmethod
    def write_yaml(datas, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            yaml.dump(datas, file, allow_unicode=True)

do_yaml = HandleYaml(CONFIG_FILE_PATH)


if __name__ == '__main__':
    # 为写入数据创建一个对象
    do_yaml = HandleYaml(CONFIG_FILE_PATH)
    # 准备写入的数据
    # datas = {
    #     'product':
    #         {'product_name': 'sofia', 'product_emmc': 'micron', 'product_cpu': 1.1},
    #     'email':
    #         {'password': 123, 'from': '123456@qq.com', 'to': '111111@qq.com'},
    #     'log':
    #         {'log_time': '[20191010, 22.33]', 'log_type': 'aplogd'}
    # }
    #
    # # yaml配置文件的读写
    # do_yaml.read_yaml('log', 'log_time')
    # do_yaml.write_yaml(datas, 'write_test_cases.yaml')