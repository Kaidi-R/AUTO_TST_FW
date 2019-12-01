# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/30 9:55 
  @Auth : 可优
  @File : test_pay.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import unittest
from unittest import mock

from Python_1128_handle_mock.payment import Payment


class PaymentTest(unittest.TestCase):
    """
    测试支付接口
    """
    def setUp(self):
        self.payment = Payment()

    def test_success(self):
        self.payment.auth = mock.Mock(return_value=200)
        res = self.payment.pay(user_id="0001", card_num="888", amount=50000)
        self.assertEqual('Success', res)

    def test_fail(self):
        self.payment.auth = mock.Mock(return_value=500)
        res = self.payment.pay(user_id="0001", card_num="888", amount=50000)
        self.assertEqual('Fail', res)

    def test_retry_success(self):
        self.payment.auth = mock.Mock(side_effect=[TimeoutError, 200])
        res = self.payment.pay(user_id="0001", card_num="888", amount=50000)
        self.assertEqual('Success', res)

    def test_retry_fail(self):
        self.payment.auth = mock.Mock(side_effect=[TimeoutError, 500])
        res = self.payment.pay(user_id="0001", card_num="888", amount=50000)
        self.assertEqual('Fail', res)


if __name__ == '__main__':
    unittest.main()

