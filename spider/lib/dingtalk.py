# coding = utf-8

import json
import logging
import spider.lib.tools
from CommonPart.combuiltin.combuiltin import ComBuiltin

'''
发送信息到钉钉--消息通知群
'''


class Dingtalk:

    def __init__(self):
        self.default_token = "4a6864baed283fe3508a81365bd706641bb392d5883257c96781111e589b29a2"
        self.product_token = "c9f523d38c86697e05ec1492e4b75f9d7bc419412480c0603f8514c8234859a4"

    async def async_message(self, mes, token=None):
        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": "快报！快报！",
                "text": mes
            },
            "at": {

                "isAtAll": False
            }
        }
        '''
        message = {
            "msgtype": "text",
            "text": {
                "content": mes
            },
            "at": {
    
                "isAtAll": True
            }
        }
        '''
        if not token:
            token = self.default_token
        message_json = json.dumps(message)
        proxies = {'http://mlj:mlj123456@120.79.183.166:9001'}

        try:
            dingtalk_url = 'https://oapi.dingtalk.com/robot/send?' \
                           f'access_token={token}'
            resp = await ComBuiltin.async_post(url=dingtalk_url, data=message_json,
                                               proxy=proxies, headers=headers, timeout=5)
            errcode = resp['errcode']  # 等于0表示成功
        except Exception as e:
            spider.lib.tools.Tools.info('钉钉异步发送信息错误:{}'.format(e))
            errcode = 1

        return errcode

    def message(self, mes, token=None):

        if not token:
            token = self.default_token

        headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

        message = {
            "msgtype": "markdown",
            "markdown": {
                "title": "通知：快报！快报！",
                "text": f"{mes}",
            },
            "at": {
                "isAtAll": False
            }
        }
        '''
        message = {
            "msgtype": "text",
            "text": {
                "content": mes
            },
            "at": {
    
                "isAtAll": True
            }
        }
        '''
        message_json = json.dumps(message)
        proxies = setting.dingtalk_proxy
        errcode = ''

        try:
            ding_url = 'https://oapi.dingtalk.com/robot/send?' \
                       f'access_token={token}'
            resp = ComBuiltin.post(url=ding_url, data=message_json, proxies=proxies,
                                   headers=headers, timeout=5)
            if resp is not None and resp.text is not None:
                errcode = json.loads(resp.text)["errcode"]  # 等于0表示成功
                errmsg = json.loads(resp.text)["errmsg"]
                if errmsg is not None:
                    logging.info(errmsg)
        except Exception as ex:
            spider.lib.tools.Tools.info(f"钉钉同步发送信息错误:{ex}")
            errcode = 1

        return errcode


if __name__ == "__main__":
    try:
        Dingtalk().message("测试")
    except Exception as e:
        spider.lib.tools.Tools.info(f"{e}")
