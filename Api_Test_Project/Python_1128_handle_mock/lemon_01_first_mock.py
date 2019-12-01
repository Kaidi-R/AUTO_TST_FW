# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/28 21:46 
  @Auth : 可优
  @File : lemon_01_first_mock.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from unittest import mock

import requests


def to_alipay():
    """
    支付宝的支付接口
    :return:
    """
    return requests.get("https://www.alipay.comdadahdodahoad/").text.encode('utf-8')


def pay():
    """
    支付功能模块
    :return:
    """
    print(to_alipay())


if __name__ == '__main__':
    to_alipay = mock.Mock(return_value='支付宝的支付接口返回成功!')
    pay()

