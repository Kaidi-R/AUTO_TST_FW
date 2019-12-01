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
    excel = HandleExcel('recharge')
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

    # 以下为请求充值接口流程
    @data(*cases)
    def test_recharge(self, case):
        # 请求url
        new_url = do_yaml.read_yaml('api', 'prefix') + case.url
        # 请求参数
        new_data = Parameterize.to_param(case.data)

        '''充值前查询账户余额'''
        # 获取excel中sql语句
        check_sql = case.check_sql
        # 如果sql存在，即excel中不为空
        if check_sql:
            # 替换参数
            check_sql = Parameterize.to_param(check_sql)
            # 获取sql查询结果
            mysql_data = self.do_mysql.run(check_sql)
            # 获取充值前的账户余额，sql数据为decimal类型，转化为浮点数
            amount_before = float(mysql_data['leave_amount'])
            # 精确到小数点后两位
            amount_before = round(amount_before, 2)

        # 发起请求
        res = self.do_request.send(new_url, data=new_data)
        # 获取实际结果
        actual_value = res.json()
        # print(res.text)

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
            # 数据校验，验证钱是否充值成功
            if check_sql:
                # 获取充值之后的账户余额
                mysql_data = self.do_mysql.run(check_sql)
                amount_later = float(mysql_data['leave_amount'])
                amount_later = round(amount_later, 2)
                #amount_later = float(actual_value['data']['leave_amount'])
                # 获取请求参数中已充值金额
                data = json.loads(new_data, encoding='utf-8')
                amount_recharge = data['amount']
                # 获取实际已充值金额
                actual_amount = round(amount_later - amount_before, 2)
                # 获取差额
                self.assertEqual(amount_recharge, actual_amount, msg='充值金额有误!')
                # do_log.error(f'{msg}充值金额有误！')

        # 断言失败，用例为fail
        except AssertionError as e:
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=fail_msg)
            do_log.error(f'{msg}的执行结果为{fail_msg}，具体异常为：{e}\n')
            # 一定要抛出异常，否则报告结果全部pass
            raise e
        # 断言成功，用例为success
        else:
            # 取出token，添加至公共请求头
            # 正常登陆的case_id为2，可以这样写，但是尽量不要把id写死
            # if case.case_id == 2:
            # 获取响应报文中的token信息
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                # Bearer后有空格
                token_headers = {'Authorization': 'Bearer ' + token}
                self.do_request.add_headers(token_headers)

            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=success_msg)
            do_log.info(f'{msg}的执行结果为{success_msg}')

if __name__ == '__main__':
    unittest.main()