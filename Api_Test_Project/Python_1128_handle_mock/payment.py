# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/11/30 9:43 
  @Auth : 可优
  @File : payment.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import requests


class Payment:
    """
    定义第三方支付类
    """
    @staticmethod
    def auth(card_num, amount):
        """
        请求第三方支付接口
        :param card_num:
        :param amount:
        :return:
        """
        url = "http://第三方支付接口.com"  # 第三方的支付接口, 不能请求
        data = {"card_num": card_num, "amount": amount}
        res = requests.post(url, data=data)
        return res.status_code

    def pay(self, user_id, card_num, amount):
        """
        支付方法
        :param user_id:
        :param card_num:
        :param amount:
        :return:
        """
        try:
            status_code = self.auth(card_num, amount)
        except TimeoutError:
            status_code = self.auth(card_num, amount)

        if status_code == 200:
            print(f"【{user_id}】支付【{amount}】成功!!! 进行扣款并登记支付记录!")
            return "Success"
        elif status_code == 500:
            print(f"【{user_id}】支付【{amount}】失败!!! 不进行扣款!")
            return "Fail"
