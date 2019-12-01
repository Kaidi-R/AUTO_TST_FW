# Author : Asura
# Email  : 1306177347@qq.com
# Let's do it!

import unittest
import json

from libs.ddt import ddt,data
from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml
from scripts.handle_parameterize import Parameterize
from scripts.handle_log import do_log

@ddt
class TestLogin(unittest.TestCase):

    # 创建对象，读取excel， 获取用例数据
    excel = HandleExcel('login')
    cases = excel.read_excel_obj()
    # 创建对象，获取公共请求头
    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.read_yaml('api', 'version'))
    # 关闭公共请求头
    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()

    # 以下为请求登录接口流程
    @data(*cases)
    def test_login(self, case):
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

        # 获取期望结果，将写入的json格式数据转化为字典类型
        expected_result = json.loads(case.expected, encoding='utf-8')
        # 断言
        try:
            self.assertEqual(expected_result.get('code'), actual_value.get('code'), msg=msg)
            self.assertEqual(expected_result.get('msg'), actual_value.get('msg'))
        # 断言失败，用例为fail
        except AssertionError as e:
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=fail_msg)
            do_log.error('{}的执行结果为{}，具体异常为{}\n'.format(msg, fail_msg, e))
            raise e
        # 断言成功，用例为success
        else:
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=success_msg)
            do_log.info('{}的执行结果为{}'.format(msg, success_msg))

if __name__ == '__main__':
    unittest.main()