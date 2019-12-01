"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import CONFIG_USERS_PATH

class Parameterize:

    # 定义待替换的正则表达式
    # 替换不存在的手机号和id以及loan_id
    not_existed_tel_pattern = r'{not_existed_tel}'
    not_existed_id_pattern = r'{not_existed_id}'
    not_existed_loan_id_pattern = r'{not_existed_loan_id}'
    # 投资人相关替换
    invest_user_tel_pattern = r'{invest_user_tel}'
    invest_user_pwd_pattern = r'{invest_user_pwd}'
    invest_user_id_pattern = r'{invest_user_id}'
    # 借款人相关替换
    borrow_user_tel_pattern = r'{borrow_user_tel}'
    borrow_user_pwd_pattern = r'{borrow_user_pwd}'
    borrow_user_id_pattern = r'{borrow_user_id}'
    # 管理人相关替换
    admin_user_tel_pattern = r'{admin_user_tel}'
    admin_user_pwd_pattern = r'{admin_user_pwd}'
    admin_user_id_pattern = r'{admin_user_id}'
    # 借款项目相关替换
    loan_id_pattern = r'{loan_id}'
    # 用户配置文件路径
    do_users_account = HandleYaml(CONFIG_USERS_PATH)

    @classmethod
    # data是待传入的参数，为excel中的data列数据
    def not_existed_replace(cls, data):
        # 创建数据库对象
        do_mysql = HandleMysql()

        # 替换不存在的手机号码
        # if re.search(cls.not_existed_tel_pattern, data):
        if cls.not_existed_tel_pattern in data:
            # sub方法替换，第一个参数为正则表达式字符串，第二个参数为替换后的新字符串，第三个参数为待替换的原始字符串
            data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)

        # 替换不存在的id
        # if re.search(cls.not_existed_id_pattern, data):
        if cls.not_existed_id_pattern in data:
            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            # 获取最大用户id + 1
            not_existed_id = do_mysql.run(sql).get('id') + 1
            data = re.sub(cls.not_existed_id_pattern, str(not_existed_id), data)

        # 替换不存在的loan_id
        # if re.search(cls.not_existed_loan_id_pattern, data):
        if cls.not_existed_loan_id_pattern in data:
            sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0,1;"
            # 获取最大标id + 1
            not_existed_loan_id = do_mysql.run(sql).get('id') + 1
            data = re.sub(cls.not_existed_loan_id_pattern, str(not_existed_loan_id), data)
        # 关闭对象
        do_mysql.close()
        return data

    @classmethod
    def invest_user_replace(cls, data):
        # 替换投资人手机号
        # if re.search(cls.invest_user_tel_pattern, data):
        if cls.invest_user_tel_pattern in data:
            data = re.sub(cls.invest_user_tel_pattern, cls.do_users_account.read_yaml('投资人', 'mobile_phone'), data)

        # 替换投资人密码
        # if re.search(cls.invest_user_pwd_pattern, data):
        if cls.invest_user_pwd_pattern in data:
            data = re.sub(cls.invest_user_pwd_pattern, cls.do_users_account.read_yaml('投资人', 'pwd'), data)

        # 替换投资人用户id
        # if re.search(cls.invest_user_id_pattern, data):
        if cls.invest_user_id_pattern in data:
            data = re.sub(cls.invest_user_id_pattern, str(cls.do_users_account.read_yaml('投资人', 'user_id')), data)

        return data

    @classmethod
    def borrow_user_replace(cls, data):
        # 替换借款人手机号
        # if re.search(cls.borrow_user_tel_pattern, data):
        if cls.borrow_user_tel_pattern in data:
            data = re.sub(cls.borrow_user_tel_pattern, cls.do_users_account.read_yaml("借款人", "mobile_phone"), data)

        # 替换借款人密码
        # if re.search(cls.borrow_user_pwd_pattern, data):
        if cls.borrow_user_pwd_pattern in data:
            data = re.sub(cls.borrow_user_pwd_pattern, cls.do_users_account.read_yaml("借款人", "pwd"), data)

        # 替换借款人用户id
        # if re.search(cls.borrow_user_id_pattern, data):
        if cls.borrow_user_id_pattern in data:
            data = re.sub(cls.borrow_user_id_pattern, str(cls.do_users_account.read_yaml("借款人", "user_id")), data)

        return data

    @classmethod
    def admin_user_replace(cls, data):
        # 替换管理人手机号
        # if re.search(cls.admin_user_tel_pattern, data):
        if cls.admin_user_tel_pattern in data:
            data = re.sub(cls.admin_user_tel_pattern, cls.do_users_account.read_yaml("管理人", "mobile_phone"), data)

        # 替换管理人密码
        # if re.search(cls.admin_user_pwd_pattern, data):
        if cls.admin_user_pwd_pattern in data:
            data = re.sub(cls.admin_user_pwd_pattern, cls.do_users_account.read_yaml("管理人", "pwd"), data)

        # 替换管理人用户id
        # if re.search(cls.admin_user_id_pattern, data):
        if cls.admin_user_id_pattern in data:
            data = re.sub(cls.admin_user_id_pattern, str(cls.do_users_account.read_yaml("管理人", "user_id")), data)

        return data

    @classmethod
    def other_replace(cls, data):
        # loan_id 替换
        # if re.search(cls.loan_id_pattern, data):
        if cls.loan_id_pattern in data:
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)
            # data = re.sub(cls.loan_id_pattern, str(getattr(cls, 'loan_id')), data)
        return data

    @classmethod
    def to_param(cls, data):

        # 类方法调用类方法，用data接收最后的结果，并且return
        data = cls.not_existed_replace(data)
        data = cls.invest_user_replace(data)
        data = cls.admin_user_replace(data)
        data = cls.borrow_user_replace(data)
        data = cls.other_replace(data)

        return data

        # # 替换不存在的手机号码
        # if re.search(cls.not_existed_tel_pattern, data):
        #     do_mysql = HandleMysql()
        #     # sub方法替换，第一个参数为正则表达式字符串，第二个参数为替换后的新字符串，第三个参数为待替换的原始字符串
        #     data = re.sub(cls.not_existed_tel_pattern, do_mysql.create_not_existed_mobile(), data)
        #     do_mysql.close()
        #
        # # 替换不存在的id
        # if re.search(cls.not_existed_id_pattern, data):
        #     do_mysql = HandleMysql()
        #     sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
        #     # 获取最大用户id + 1
        #     not_existed_id = do_mysql.run(sql).get('id') + 1
        #     data = re.sub(cls.not_existed_id_pattern, str(not_existed_id), data)
        #     do_mysql.close()
        #
        # # 替换不存在的loan_id
        # if re.search(cls.not_existed_loan_id_pattern, data):
        #     do_mysql = HandleMysql()
        #     sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0,1;"
        #     # 获取最大标id + 1
        #     not_existed_loan_id = do_mysql.run(sql).get('id') + 1
        #     data = re.sub(cls.not_existed_loan_id_pattern, str(not_existed_loan_id), data)
        #     do_mysql.close()
        #
        # # 替换投资人手机号
        # if re.search(cls.invest_user_tel_pattern, data):
        #     data = re.sub(cls.invest_user_tel_pattern, cls.do_users_account.read_yaml('投资人', 'mobile_phone'), data)
        #
        # # 替换投资人密码
        # if re.search(cls.invest_user_pwd_pattern, data):
        #     data = re.sub(cls.invest_user_pwd_pattern, cls.do_users_account.read_yaml('投资人', 'pwd'), data)
        #
        # # 替换投资人用户id
        # if re.search(cls.invest_user_id_pattern, data):
        #     data = re.sub(cls.invest_user_id_pattern, str(cls.do_users_account.read_yaml('投资人', 'user_id')), data)
        #
        # # 替换借款人手机号
        # if re.search(cls.borrow_user_tel_pattern, data):
        #     data = re.sub(cls.borrow_user_tel_pattern, cls.do_users_account.read_yaml("借款人", "mobile_phone"), data)
        #
        # # 替换借款人密码
        # if re.search(cls.borrow_user_pwd_pattern, data):
        #     data = re.sub(cls.borrow_user_pwd_pattern, cls.do_users_account.read_yaml("借款人", "pwd"), data)
        #
        # # 替换借款人用户id
        # if re.search(cls.borrow_user_id_pattern, data):
        #     data = re.sub(cls.borrow_user_id_pattern, str(cls.do_users_account.read_yaml("借款人", "user_id")), data)
        #
        # # 替换管理人手机号
        # if re.search(cls.admin_user_tel_pattern, data):
        #     data = re.sub(cls.admin_user_tel_pattern, cls.do_users_account.read_yaml("管理人", "mobile_phone"), data)
        #
        # # 替换管理人密码
        # if re.search(cls.admin_user_pwd_pattern, data):
        #     data = re.sub(cls.admin_user_pwd_pattern, cls.do_users_account.read_yaml("管理人", "pwd"), data)
        #
        # # 替换管理人用户id
        # if re.search(cls.admin_user_id_pattern, data):
        #     data = re.sub(cls.admin_user_id_pattern, str(cls.do_users_account.read_yaml("管理人", "user_id")), data)
        #
        # # loan_id 替换
        # if re.search(cls.loan_id_pattern, data):
        #     loan_id = getattr(cls, 'loan_id')
        #     data = re.sub(cls.loan_id_pattern, str(loan_id), data)
        #     # data = re.sub(cls.loan_id_pattern, str(getattr(cls, 'loan_id')), data)
        #
        # return data

if __name__ == '__main__':
    # 注册接口参数化
    one_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}'
    two_str = '{"mobile_phone": "", "pwd": "12345678"}'
    three_str = '{"mobile_phone": "{not_existed_tel}", "pwd": "12345678901234567", "reg_name": "KeYou"}'
    four_str = '{"mobile_phone": "{invest_user_tel}", "pwd": "12345678", "reg_name": "KeYou"}'

    print(Parameterize.to_param(one_str))
    print(Parameterize.to_param(two_str))
    print(Parameterize.to_param(three_str))
    print(Parameterize.to_param(four_str))

    # param = Parameterize()
    # print(param.to_param(one_str))
    # print(param.to_param(two_str))
    # print(param.to_param(three_str))
    # print(param.to_param(four_str))