# coding = utf-8

class JsonFormat(object):
    """
    json序列化和反序列化的辅助类
    """

    def convert_to_builtin_type(obj):
        d = {}
        try:
            d.update(obj.__dict__)
        except Exception:
            return d
        return d