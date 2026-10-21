"""计算字符串的显示宽度：东亚宽字符按 2 列计，用于同列对齐。"""

import unicodedata


def display_width(text):
    """返回字符串在等宽字体下占用的列数。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1
               for ch in text)
