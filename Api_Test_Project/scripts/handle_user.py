"""
===========================
Author:帅迪
Time:2019/11/22
Mail:1306177347@qq.com
===========================
"""

from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import do_yaml
from scripts.handle_path import CONFIG_USERS_PATH

# 定义注册新用户的函数，注册名、密码、type需要当作参数传入，
# 并和手机号一起当作接口请求的参数
def create_new_user(reg_name, pwd='123456789', user_type=1):
    # 定义接口请求对象和数据库查询对象
    do_request = HandleRequest()
    do_mysql = HandleMysql()

    # 获取请求url
    url = do_yaml.read_yaml('api', 'prefix') + '/member/register'
    # 获取sql查询语句
    sql = do_yaml.read_yaml('mysql', 'select_user_id_sql')

    # 构造请求头
    do_request.add_headers(do_yaml.read_yaml('api', 'version'))

    while True:
    # 请求需要传参url，以及请求参数，请求参数中手机号码和密码必填
        mobile_phone = do_mysql.create_not_existed_mobile()
        # 构造请求参数
        # data = {'mobile_phone': mobile_phone, 'pwd': pwd, 'reg_name': reg_name, 'type': user_type}
        data = {'reg_name': reg_name, 'pwd': pwd, 'type': user_type, 'mobile_phone': mobile_phone}
        # 发起请求
        do_request.send(url, data=data)

        # 注册后从数据库查询，并获取用户id，数据库查询存在break
        exist_result = do_mysql.run(sql, mobile_phone)
        if exist_result:
            user_id = exist_result['id']
            break

    # 构造需要写入到yaml的字典
    user_dict = {reg_name:{'reg_name': reg_name, 'user_id': user_id, 'mobile_phone': mobile_phone, 'pwd':pwd, }}
    # 关闭创建的对象
    do_request.close()
    do_mysql.close()
    # 返回构造需要写入到yaml的字典
    return user_dict

def create_users_info():
    # 生成借款人，投资人，管理人三个用户的信息
    users_data = {}
    users_data.update(create_new_user('借款人'))
    users_data.update(create_new_user('投资人'))
    users_data.update(create_new_user('管理人', user_type=0))
    do_yaml.write_yaml(users_data, CONFIG_USERS_PATH)

if __name__ == '__main__':
    create_users_info()
