# coding = utf-8

class Headers(object):
    """
    项目专用的请求头存储类
    """

    def header(**kwargs):
        """
        获取fin.bop.weibo.com类型网站的header
        :param kwargs: cookie
        :return:
        """
        return {
            'authority': 'm.weibo.cn',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'x-xsrf-token': 'ab487a',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.51 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://m.weibo.cn/detail/{mid}'.format(**kwargs),
            'mweibo-pwa': '1',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'sec-fetch-site': 'same-origin',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
            'cookie': "{cookie_str}".format(**kwargs),
        }
