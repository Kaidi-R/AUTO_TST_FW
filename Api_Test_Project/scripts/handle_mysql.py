"""
===========================
Author:帅迪
Time:2019/11/18
Mail:1306177347@qq.com
===========================
"""

import pymysql
import random

from scripts.handle_yaml import do_yaml

class HandleMysql():

    def __init__(self):
        # 建立一个数据库连接对象
        self.conn = pymysql.connect(host=do_yaml.read_yaml('mysql', 'host'),
                                    port=do_yaml.read_yaml('mysql', 'port'),
                                    user=do_yaml.read_yaml('mysql', 'user'),
                                    password=do_yaml.read_yaml('mysql', 'password'),
                                    database=do_yaml.read_yaml('mysql', 'database'),
                                    charset='utf8',
                                    # 默认返回结果为元组或者嵌套元组的列表，
                                    # 指定这个类后返回结果为字典或者嵌套字典的列表
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
        # 建立一个数据库游标对象
        self.cursor = self.conn.cursor()

    # 定义一个获取一个或多个数据库命令执行结果的方法
    def run(self, sql, params=None, is_more=False):
        # 游标对象执行
        self.cursor.execute(sql, params)
        # 连接对象提交
        self.conn.commit()
        # 返回结果
        if is_more:
            return self.cursor.fetchall()
        else:
            return  self.cursor.fetchone()

    # 关闭游标对象和连接对象
    def close(self):
        self.cursor.close()
        self.conn.close()

    # 随机生成一个188开头的手机号码
    @staticmethod
    def create_mobile():
        return '188' + ''.join(random.sample('0123456789', 8))

    # 判断手机号是否被注册，数据库中是否有该手机号
    def is_existed_mobile(self, mobile):
        sql = do_yaml.read_yaml('mysql', 'select_user_sql')
        if self.run(sql, params=[mobile]):
            return True
        else:
            return False

    # 随机生成一个在数据库中不存在的手机号
    def create_not_existed_mobile(self):
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

if __name__ == '__main__':
    do_mysql = HandleMysql()
    print(do_mysql.create_not_existed_mobile())
    do_mysql.close()








