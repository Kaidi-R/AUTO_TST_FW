"""
===========================
Author:帅迪
Time:2019/11/22
Mail:1306177347@qq.com
===========================
"""
import unittest

from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import do_yaml
from libs.ddt import ddt,data
from scripts.handle_parameterize import Parameterize
from scripts.handle_log import do_log

@ddt
class TestRegister(unittest.TestCase):

    # 创建对象，读取excel， 获取用例数据
    excel = HandleExcel('register')
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

    # 以下为请求注册接口流程
    @data(*cases)
    def test_register(self, case):
        # 请求url
        new_url = do_yaml.read_yaml('api', 'prefix') + case.url
        #print(new_url)
        # 请求参数
        new_data = Parameterize.to_param(case.data)
        #print(new_data)
        # 发起请求
        res = self.do_request.send(new_url, data=new_data)
        # 获取实际结果
        actual_value = res.json()
        #print(actual_value)

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
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'actual_col'), value=res.text)
            self.excel.write_excel(row=row, column=do_yaml.read_yaml('excel', 'result_col'), value=success_msg)
            do_log.info(f'{msg}的执行结果为{success_msg}')

        # 从excel读取用户数据，注册之后写入yaml
        # do_yaml.write_yaml({'{}_info'.format(actual_value['data']['reg_name']): actual_value.get('data')}, os.path.join(CONFIGS_DIR, 'user_info.yaml'))

if __name__ == '__main__':
    unittest.main()




