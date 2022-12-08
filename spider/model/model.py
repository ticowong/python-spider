# _*_ coding:utf-8 _*_

import asyncio
import logging
from pymysql import escape_string
from spider.lib.tools import Tools
from spider.lib.database import DataBase
from spider.controller.database import DataBaseController


class Model(DataBase):
    """
    数据模型 Model
    """

    def database_name(self):
        logging.error(f"请重写函数{__class__}.database_name，并返回对应数据库的名称")
        return ""

    def table_name(self):
        logging.error(f"请重写函数{__class__}.table_name，并返回模型对应数据表的名称")
        return ""

    def columns4save(self):
        """保存数据时的字段"""
        logging.error(f"请重写函数{__class__}.columns4save，并返回保存数据的字段字符串，英文逗号分隔")
        return ''

    def columns4update(self):
        """遇到相同数据时需要更新的字段"""
        return ''

    def build_upsert_sql(self, camel_values=True, upper_first=False, **kwargs):
        """根据columns4save函数返回的字符串和columns4update返回的字符串，创建upsert语句"""
        sql = "insert into {table_names} ({save_columns}) " \
              "values ({save_values}) " \
              "ON DUPLICATE KEY UPDATE {update_columns}"

        columns = self.columns4save()
        save_columns = ""
        tmp_list = columns.split(",")
        for col in tmp_list:
            col = col.strip(" ")
            if camel_values:
                tmp_col = Tools.name_convert_to_camel(col, upper_first)
                if kwargs and tmp_col not in kwargs.keys():
                    continue
            else:
                if kwargs and col not in kwargs.keys():
                    continue
            if save_columns:
                save_columns = f"{save_columns},`{col}`"
            else:
                save_columns = f"`{col}`"
        save_values = ""
        tmp_list = columns.split(",")
        for col in tmp_list:
            col = col.strip(" ")
            if camel_values:
                tmp_col = Tools.name_convert_to_camel(col, upper_first)
                if kwargs and tmp_col not in kwargs.keys():
                    continue
                col_values = "{start}{col}{end}".format(col=tmp_col, start="{", end="}")
            else:
                if kwargs and col not in kwargs.keys():
                    continue
                col_values = "{start}{col}{end}".format(col=col, start="{", end="}")
            if save_values:
                save_values = f"{save_values},'{col_values}'"
            else:
                save_values = f"'{col_values}'"

        update = self.columns4update()
        update_columns = ""
        tmp_list = update.split(",")
        for col in tmp_list:
            col = col.strip(" ")
            if camel_values:
                tmp_col = Tools.name_convert_to_camel(col, upper_first)
                if kwargs and tmp_col not in kwargs.keys():
                    continue
                col_values = "{start}{col}{end}".format(col=tmp_col, start="{", end="}")
            else:
                if kwargs and col not in kwargs.keys():
                    continue
                col_values = "{start}{col}{end}".format(col=col, start="{", end="}")
            if update_columns:
                update_columns = f"{update_columns},`{col}`='{col_values}'"
            else:
                update_columns = f"`{col}` = '{col_values}'"
        params = {
            "table_names": self.table_name(),
            "save_columns": save_columns,
            "save_values": save_values,
            "update_columns": update_columns
        }
        tmp = sql.format(**params)
        return tmp

    def escape_strings(self, **kwargs):
        tmp = dict()
        for item in kwargs:
            if type(kwargs[item]) is str:
                tmp[item] = escape_string(kwargs[item])
            else:
                tmp[item] = kwargs[item]
        return tmp

    async def get_list(self, str_select, str_from="", str_where=""):
        """获取数据列表"""
        if not str_select:
            str_select = self.columns4save()
        if not str_from:
            str_from = self.table_name()
        sql = f"select {str_select} " \
              f"from {str_from} " \
              f"{str_where}"
        res = await DataBase().list(self.database_name(), sql)
        logging.info(f"执行SQL：。{sql}")
        if res:
            logging.info(f"获取数据成功。{__file__}")
            return res
        else:
            logging.info(f"获取数据失败。{__file__}")
        return None

    async def get_one_dict(self, str_select="", str_from="", str_where=""):
        """
        根据传入的select字符串，返回字段对应数据的dict数据
        :param str_select:
        :param str_from:
        :param str_where:
        :return:
        """
        if not str_select:
            str_select = self.columns4save()
        if not str_from:
            str_from = self.table_name()
        sql = f"select {str_select} " \
              f"from {str_from} " \
              f"{str_where}"
        dbname = self.database_name()
        logging.info(f"准备执行SQL：。{sql}")
        res = await DataBase().one(dbname, sql)
        logging.info(f"执行SQL：。{sql}")
        if res:
            logging.info(f"获取数据成功。{__file__}")
            cols = str.split(str_select, ',')
            if len(cols) >= 1:
                res_tmp = {}
                index = 0
                for col in cols:
                    res_tmp[col] = res[index]
                    index += 1
                return res_tmp
            return res
        else:
            logging.info(f"获取数据失败。{__file__}")
        return None

    async def get_list_dict(self, str_select, str_from="", str_where=" limit 100"):
        """
        根据传入的select字段返回字段对应数据的dict数据列表
        :param str_select:
        :param str_from:
        :param str_where:
        :return:
        """
        if not str_select:
            str_select = self.columns4save()
        if not str_from:
            str_from = self.table_name()
        sql = f"select {str_select} " \
              f"from {str_from} " \
              f"{str_where}"
        dbname = self.database_name()
        res = await DataBase().list(dbname, sql)
        logging.info(f"执行SQL：。{sql}")
        if res:
            logging.info(f"获取数据成功。{__file__}")
            cols = str.split(str_select, ',')
            if len(cols) >= 1:
                res_tmp = []
                for item in res:
                    index = 0
                    res_tmp_1 = {}
                    for col in cols:
                        res_tmp_1[col] = item[index]
                        index += 1
                    res_tmp.append(res_tmp_1)
                return res_tmp
            return res
        else:
            logging.info(f"获取数据失败。{__file__}")
        return None

    async def save(self, obj, camel_values=False, upper_first=False):
        """保存数据"""
        try:
            sql = self.build_upsert_sql(camel_values, upper_first, **obj).format(**self.escape_strings(**obj))
            await DataBaseController().push(sql)
            logging.info(f"保存SQL：。{sql}")
        except Exception as ex:
            logging.error(f"{__file__}.save: {ex}")

    async def push(self, sql):
        try:
            await DataBaseController().push(sql)
            logging.info(f"保存SQL：。{sql}")
        except Exception as ex:
            logging.error(f"{__file__}.save: {ex}")


async def test():
    tmp = Model().build_upsert_sql()
    logging.info(tmp)
    await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(test())
    import time

    time.sleep(2)
    exit(0)
