# coding = utf-8

import logging

from spider.lib.tools import Tools
from spider.lib.database import DataBase


class Cookie(object):
    """
    专用的读取和设置cookie的类
    ⚠️注意：默认会在数据库里的uid会加上-fin后缀以区分是否掘金专用cookie
    kwargs: ext默认后缀为-fin
    """

    def __init__(self, **kwargs):
        self.ext = kwargs.pop("ext", "")

    async def get(self, uid):
        """
        获取指定uid的cookie
        :return:
        """
        cursor = await DataBase.pool("mansys")
        sql = "select cookie from ms_cookie " \
              "where uid = '{uid}{ext}'".format(uid=uid, ext=self.ext)
        r = await cursor.select(sql)
        if r:
            return r[0][0]
        return None

    async def set(self, uid, cookie_str):
        """
        保存cookie到数据库
        :param cookie_str:
        :return:
        """
        if cookie_str is None or cookie_str == "None":
            Tools.info(f'传入cookie_str为空，不保存...')
        else:
            uid_exists = await self.get(uid)
            if uid_exists:
                await self.update(uid, cookie_str)
            else:
                await self.add(uid, cookie_str)

    async def add(self, uid, cookie_str):
        """
        添加cookie数据
        :param cookie_str:
        :return:
        """
        try:
            cursor = await DataBase.pool("mamsys")
            sql = "insert into ms_cookie(`cookie`, `uid`)" \
                  "values('{cookie_str}','{uid}{ext}')" \
                .format(uid=uid, cookie_str=cookie_str, ext=self.ext)
            r = await cursor.execute(sql)
            return r
        except Exception as e:
            logging.info(f"添加cookie数据出错{e}")
            return None

    async def update(self, uid, cookie_str):
        """
        更新cookie数据
        :param cookie_str:
        :return:
        """
        try:
            pool = await DataBase.pool()
            cursor = pool["mansys"]
            sql = "update ms_cookie " \
                  "set `cookie` = '{cookie_str}' " \
                  "where `uid` = '{uid}{ext}'" \
                .format(uid=uid, cookie_str=cookie_str, ext=self.ext)
            r = await cursor.execute(sql)
            return r
        except Exception as e:
            Tools.info(f"更新cookie数据出错{e}")
            return None
