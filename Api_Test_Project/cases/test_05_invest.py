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
class TestInvest(unittest.TestCase):

    # 创建对象，读取excel， 获取用例数据
    excel = HandleExcel('invest')
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

    # 以下为请求投资接口流程
    @data(*cases)
    def test_invest(self, case):
        # 请求url
        new_url = do_yaml.read_yaml('api', 'prefix') + case.url
        # 请求参数
        new_data = Parameterize.to_param(case.data)
        # 发起请求
        # res = self.do_request.send(new_url, data=new_data)
        res = self.do_request.send(url=new_url, method=case.method, data=new_data)
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
            # 正常登陆的case_id为1,3,5，可以这样写，但是尽量不要把id写死
            # if case.case_id in [1,3,5]:
            # 获取响应报文中的token信息
            if 'token_info' in res.text:
                token = actual_value['data']['token_info']['token']
                token_headers = {'Authorization': 'Bearer ' + token}
                self.do_request.add_headers(token_headers)

            '''取出load_id的第一种方法'''
            # 获取excel中sql语句
            check_sql = case.check_sql
            # 如果sql存在，即excel中不为空
            # if check_sql:
            #     # 替换参数
            #     check_sql = Parameterize.to_param(check_sql)
            #     # 获取sql查询结果
            #     mysql_data = self.do_mysql.run(check_sql)
            #     # 获取数据库中的load_id
            #     load_id = mysql_data['id']
            #     # 动态创建属性的机制, 来解决接口依赖的问题
            #     # 给Parameterize类中的loan_id类属性设置其值为load_id
            #     setattr(Parameterize, 'loan_id', load_id)

            '''取出load_id的第二种方法'''
            # 借款人加标的case_id为2
            # if case.case_id == 2:
            #     load_id = actual_value.get('data').get('id')
            #     setattr(Parameterize, 'loan_id', load_id)

            '''取出load_id的第三种方法'''
            # 将check_sql列设计为json格式，设计键值对并将sql语句设为键值，进行sql语句的选用
            check_sql = case.check_sql
            # 如果sql存在，即excel中不为空
            if check_sql:
                # 替换参数
                check_sql = Parameterize.to_param(check_sql)
                # json格式转化为字典
                check_sql = json.loads(check_sql, encoding='utf-8')
                # 利用键名进行判断
                if 'loan' in check_sql:
                    mysql_data = self.do_mysql.run(check_sql['loan'])
                    load_id = mysql_data['id']
                    setattr(Parameterize, 'loan_id', load_id)


            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=success_msg)
            do_log.info(f'{msg}的执行结果为{success_msg}')

if __name__ == '__main__':
    unittest.main()