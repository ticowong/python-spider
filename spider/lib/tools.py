# _*_ coding:utf-8 _*_

"""
工具类
"""
import re
import os
import time
import json
import logging

import CommonPart.commonvar.commonvar

import setting
import spider.lib


class Tools:

    @staticmethod
    def dict_get(dict, key, *args):
        """
        取字典指定key的值，找不到则返回第三个参数
        """
        if not dict:
            if args:
                return args[0]
            else:
                return None
        if type(dict) is list:
            return dict[key]
        if type(key) is int:
            return dict[key]
        if key in dict:
            tmp = dict.get(key)
            if tmp:
                return tmp
        if type(key) is int:
            if key in dict:
                return dict[key]
            else:
                return dict[str(key)]
        if args:
            return args[0]

    @staticmethod
    def info(msg, **kwargs):
        """
        自定义的logging.info封装函数
        :param kwargs: level，错误等级默认为0，展示所有提示信息，数字越大错误等级越高，
        暂定0为所有都提示，1为notice级，2为warning级,3为error级,4为钉钉通知级别
        :return:
        """
        level = Tools.dict_get(kwargs, "level", 1)
        if level >= setting.logging_level:
            logging.info(msg)
        if level == 4:
            spider.lib.Dingtalk().message("{}:{}".format(Tools.get_time(), msg))

    @staticmethod
    def get_date(*args):
        """
        获取系统当前日期
        :return: 2020-02-02
        """
        day = len(args) > 0 and args[0] or 0
        return time.strftime('%Y-%m-%d', time.localtime(time.time() + day * 60 * 60 * 24))

    @staticmethod
    def get_time(*args):
        """
        获取系统当前时间
        :return: 2020-02-02
        """
        seconds = len(args) > 0 and args[0] or 0
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + seconds))

    @staticmethod
    def hex_trans(nx, x1, x):
        """
        将字符串从x1进制转换成x进制数据，x范围为2到62
        :param x1:
        :param x:
        :return:
        """
        # n为待转换的十进制数，x为机制，取值为2-62
        a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
             'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        nx = str(nx)
        b1 = list(nx)
        # print(nx, "[", x1, "]==[", x, "] ", end='')
        b2 = []
        for i in b1:
            for i1 in range(0, 62):
                if a[i1] == i:
                    b2 = b2 + [i1]
                    if i1 > x1:
                        print(i, "错误定义")
        b2.reverse()
        # print(b2)
        n1 = 0
        n2 = 1
        for i in b2:
            n1 = n1 + int(i) * (pow(x1, n2 - 1))  # pow(x, n)，即计算 x 的 n 次幂函数
            n2 = n2 + 1
            # print (n1,n2)
        n = n1
        # print(n)
        b = []
        while True:
            s = n // x  # 商
            y = n % x  # 余数
            b = b + [y]
            if s == 0:
                break
            n = s
        b.reverse()  # reverse() 函数用于反向列表中元素,由个，十百转为百十个
        bd = ""
        for i in b:
            # print(a[i],end='')
            bd = bd + a[i]
        # print(bd)
        return bd

    @staticmethod
    def str2mid(str):
        """
        根据str_mid转换成mid
        :return:
        """
        if not str:
            return ""
        if len(str) < 5:
            return ""
        # Tools.info('str2mid: ' + str)
        res = '{}{}{}'.format(
            Tools.hex_trans(str[0:1], 62, 10).zfill(2),
            Tools.hex_trans(str[1:5], 62, 10).zfill(7),
            Tools.hex_trans(str[5:len(str)], 62, 10).zfill(7),
        )
        # Tools.info('result: ' + res)
        return res

    @staticmethod
    def mid2str(mid):
        """
        根据str_mid转换成str_mid
        :return:
        """
        if not mid:
            return ""
        if len(mid) < 5:
            return ""
        # Tools.info('mid2str: ' + mid)
        res = '{}{}{}'.format(
            Tools.hex_trans(mid[0:2], 10, 62),
            Tools.hex_trans(mid[2:9], 10, 62),
            Tools.hex_trans(mid[9:len(mid)], 10, 62),
        )
        # Tools.info('result: ' + res)
        return res

    @staticmethod
    def get_mid_from_text(text):
        """
        根据备注获取博文str_mid
        :return:
        """
        if not text:
            return ""
        Tools.info(text)
        match_obj = re.search(r'\/(\d+)\/([^\"\']+)', text, re.M | re.I)
        if match_obj:
            Tools.info(match_obj.group(2))
            return match_obj.group(2)
        return ""

    @staticmethod
    def get_order_id_from_text(text):
        """
        根据字符串获取粉丝头条订单
        :return:
        """
        if not text:
            return ""
        Tools.info(text)
        match_obj = re.search(r'订单(\d+)', text, re.M | re.I)
        if match_obj:
            Tools.info(match_obj.group(1))
            return match_obj.group(1)
        return ""

    @staticmethod
    def get_uid_from_url(url):
        """
        根据url获取微博uid
        :return:
        """
        if not url:
            return ""
        Tools.info(url)
        match_obj = re.search(r'\.com\/(\d+)\/([^\"\']+)', url, re.M | re.I)
        if match_obj:
            Tools.info(match_obj.group(1))
            return match_obj.group(1)
        return ""

    @staticmethod
    def project_root_path(project_name=None, print_log=False):
        """
        获取当前项目根路径
        :param project_name: 项目名称
                                1、可在调用时指定
                                2、[推荐]也可在此方法中直接指定 将'XmindUitl-master'替换为当前项目名称即可（调用时即可直接调用 不用给参数）
        :param print_log: 是否打印日志信息
        :return: 指定项目的根路径
        """
        p_name = CommonPart.commonvar.commonvar.CommonVar.model_name if project_name is None else project_name
        project_path = os.path.abspath(os.path.dirname(__file__))
        # Windows
        if project_path.find('\\') != -1: separator = '\\'
        # Mac、Linux、Unix
        if project_path.find('/') != -1: separator = '/'

        root_path = project_path[:project_path.find(f'{p_name}{separator}') + len(f'{p_name}{separator}')]
        if print_log: print(f'当前项目名称：{p_name}\r\n当前项目根路径：{root_path}')
        return root_path

    @staticmethod
    def name_convert_to_camel(name: str, upper_first=False) -> str:
        """下划线转驼峰(小驼峰)"""
        tmp = re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)
        if upper_first:
            return "{}{}".format(str.upper(tmp[0:1]), tmp[1:])
        else:
            return tmp

    @staticmethod
    def name_convert_to_snake(name: str) -> str:
        """驼峰转下划线"""
        if '_' not in name:
            name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        return name.lower()

    @staticmethod
    def name_convert(name: str) -> str:
        """驼峰式命名和下划线式命名互转"""
        is_camel_name = True  # 是否为驼峰式命名
        if '_' in name and re.match(r'[a-zA-Z_]+$', name):
            is_camel_name = False
        # elif re.match(r'[a-zA-Z]+$', name) is None:
        #     raise ValueError(f'Value of "name" is invalid: {name}')
        return Tools.name_convert_to_snake(name) if is_camel_name else Tools.name_convert_to_camel(name)

    @staticmethod
    async def get_token(str_ext=""):
        redis = await spider.lib.Redis().pool()
        json_str = await redis.execute("get", f"{CommonPart.commonvar.commonvar.CommonVar.model_name}:token{str_ext}")
        if json_str:
            json_obj = json.loads(json_str)
            if json_obj:
                return json_obj

    @staticmethod
    async def set_token(str_ext="", value=""):
        redis = await spider.lib.Redis().pool()
        json_str = await redis.execute("set", f"{CommonPart.commonvar.commonvar.CommonVar.model_name}:token{str_ext}",
                                       json.dumps(value))
        if json_str:
            return json_str


if __name__ == "__main__":
    Tools.info(Tools.get_uid_from_url('http://weibo.com/6783801313/Ljq9F5K4X'))
    Tools.info(Tools.str2mid("LiWJHmQe5"))
    Tools.get_order_id_from_text(
        'asfjidla;fjdaf;jdkla https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fpassport.weibo.com%2Fwbsso%2Flogout%3Fr%3Dhttp%253A%252F%252Ffin.bop.weibo.com%252Fclient%252Fsignout%26returntype%3D1&#39;')
    Tools.info(Tools.get_date(-1))
    Tools.info(Tools.get_time())
    Tools.info(Tools.dict_get({"test_key": "test_value"}, "test_key_no_exists"))
    Tools.info(Tools.dict_get({"test_key": "test_value"}, "test_key", "default_value"))
    Tools.info(Tools.dict_get({"test_key": "test_value"}, "test_key_no_exists", "default_value"))
