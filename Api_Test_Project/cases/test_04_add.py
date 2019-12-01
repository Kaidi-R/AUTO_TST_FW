"""
===========================
Author:帅迪
Time:2019/11/23
Mail:1306177347@qq.com
===========================
"""

import unittest
import json

from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml
from libs.ddt import ddt,data
from scripts.handle_parameterize import Parameterize
from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql

@ddt
class TestRecharge(unittest.TestCase):

    # 创建对象，读取excel， 获取用例数据
    excel = HandleExcel('add')
    cases = excel.read_excel_obj()
    # 创建对象，获取公共请求头
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.read_yaml('api', 'version'))
        cls.do_mysql = HandleMysql()
    # 关闭公共请求头
    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close()

    # 以下为请求加标接口流程
    @data(*cases)
    def test_recharge(self, case):
        # 请求url
        new_url = do_yaml.read_yaml('api', 'prefix') + case.url
        # 请求参数
        new_data = Parameterize.to_param(case.data)
        # 发起请求
        res = self.do_request.send(new_url, data=new_data)
        # 获取实际结果
        actual_value = res.json()

        # 获取写入excel的行号
        row = case.case_id + 1
        # 获取提示信息
        msg = case.title
        success_msg = do_yaml.read_yaml('msg', 'success_result')
        fail_msg = do_yaml.read_yaml('msg', 'fail_result')

        # 获取期望结果
        expected_result = case.expected
        # 断言
        try:
            self.assertEqual(expected_result, actual_value.get('code'), msg=msg)
        # 断言失败，用例为fail
        except AssertionError as e:
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=fail_msg)
            do_log.error(f'{msg}的执行结果为{fail_msg}，具体异常为：{e}\n')
            raise e
        # 断言成功，用例为success
        else:
            # 取出token，添加至公共请求头
            # 正常登陆的case_id为2，可以这样写，但是尽量不要把id写死
            # if case.case_id == 2:
            # 获取响应报文中的token信息
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                token_headers = {'Authorization': 'Bearer ' + token}
                self.do_request.add_headers(token_headers)

            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=success_msg)
            do_log.info(f'{msg}的执行结果为{success_msg}')

if __name__ == '__main__':
    unittest.main()