"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import requests
import json

class HandleRequest():
    # 定义一个会话对象
    def __init__(self):
        self.one_session = requests.Session()
    # 添加公共请求头
    def add_headers(self, headers):
        self.one_session.headers.update(headers)
    # 发起请求，参数为url、请求方式、参数data以及不定长参数，
    # 不定长参数可以传关键字参数headers、params、files等
    def send(self, url, method='post', data=None, is_json=True, **kwargs):
        # 判断参数data是否为字符串
        if isinstance(data, str):
            # 如果是json格式字符串则转化为字典
            try:
                data = json.loads(data)
            # 如果是字典类型字符串则转化为字典
            except Exception as e:
                print('记录日志')
                data = eval(data)

        # 将请求方式统一转化为小写
        method = method.lower()
        # 请求方式为get，没有请求体，传参给params，查询字符串参数
        if method == 'get':
            res = self.one_session.request(method, url, params=data, **kwargs)
        # 这几种请求方式均有请求体
        elif method in ('post', 'put', 'delete', 'patch'):
            # 传参给json，传参方式为json
            if is_json:
                res = self.one_session.request(method, url, json=data, **kwargs)
            # 否则传参给data，传参方式为www-from表单
            else:
                res = self.one_session.request(method, url, data=data, **kwargs)
        # 如果请求方式以上都不是，返回一个None
        else:
            res = None
            print('不支持【{}】'.format(method))
        return res

    # 关闭会话对象，释放资源
    def close(self):
        self.one_session.close()

# 定义一个简单版的请求封装
# class HandleRequest1():
#
#     def __init__(self):
#         self.one_session = requests.Session()
#
#     def send(self, method, url, **kwargs):
#         method = method.lower()
#         if method in ('get','post', 'put', 'delete', 'patch'):
#             res = self.one_session.request(method, url, **kwargs)
#         else:
#             res = None
#             print(f'不支持【{method}】方法')
#         return res
#
#     def close(self):
#         self.one_session.close()

if __name__ == '__main__':
    # 登录 url 参数 请求头
    login_url = 'http://api.lemonban.com/futureloan/member/login'
    login_params = '{"mobile_phone": "18244446667","pwd": "12345678"}'
    headers = {"User-Agent": "Mozilla/5.0 KeYou","X-Lemonban-Media-Type": "lemonban.v2"}
    # 登录
    do_request = HandleRequest()
    do_request.add_headers(headers)
    login_res = do_request.send(login_url, method='post', data=login_params, is_json=True)
    # 获取id token
    json_datas = login_res.json()
    # json_datas = json.loads(login_res)
    member_id = json_datas['data']['id']
    token = json_datas['data']['token_info']['token']

    # 充值 url 参数 请求头
    recharge_url = 'http://api.lemonban.com/futureloan/member/recharge'
    recharge_params = {"member_id": member_id,"amount": "10000"}
    # recharge_params = '{"member_id": member_id,"amount": "50000","code": True}'
    token_header = {"Authorization": "Bearer " + token}
    # 充值
    do_request.add_headers(token_header)
    recharge_res = do_request.send(recharge_url, method='post' ,data=recharge_params)





