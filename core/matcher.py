# 通配符模式
import fnmatch
def match_any(name, patterns):
    """名字是否命中任意一个通配符模式；无通配符时等价于字符串相等。

    示例：'*.jpg' 匹配图片，'*v' 匹配以 v 结尾的文件夹名。
    """
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)
