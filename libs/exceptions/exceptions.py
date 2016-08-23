class ResourceMergerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadArgumentException(ResourceMergerException):
    pass


class BadMergeException(ResourceMergerException):
    pass
