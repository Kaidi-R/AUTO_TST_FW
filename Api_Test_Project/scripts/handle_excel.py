"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import openpyxl
import os

from scripts.handle_path import DATAS_DIR
from scripts.handle_yaml import do_yaml

# 定义测试用例对象类
class CaseData():
    pass

# 定义excel类
class HandleExcel():
    # 参数为文件名和表单名
    def __init__(self, sheetname, filename=None):
        # 如果用户没有传文件名，则打开路径下的文件
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read_yaml("excel", "cases_path"))
        else:
            self.filename = filename
        self.sheetname = sheetname
    # 打开文件和表单
    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheetname]

    # 读取用例数据
    def read_excel(self):
        self.open()
        # 获取全部用例数据
        rows = list(self.sh.rows)
        # 分别遍历表头和用例数据，打包添加用例至列表
        cases = []
        title = [i.value for i in rows[0]]
        for j in rows[1:]:
            data = [k.value for k in j]
            case_data = dict(zip(title, data))
            cases.append(case_data)
        self.wb.close()
        return cases

    def read_excel_obj(self):
        self.open()
        # 获取全部用例数据
        rows = list(self.sh.rows)
        # 分别遍历表头和用例数据，打包添加用例至列表
        cases = []
        title = [i.value for i in rows[0]]
        for j in rows[1:]:
            data = [k.value for k in j]
            case = CaseData()
            for v in zip(title, data):
                setattr(case, v[0], v[1])
            cases.append(case)
        self.wb.close()
        return cases

    # 写入用例数据
    def write_excel(self, row, column, value):
        self.open()
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)
        self.wb.close()

if __name__ == '__main__':
    read = HandleExcel('register')
    read.read_excel()




