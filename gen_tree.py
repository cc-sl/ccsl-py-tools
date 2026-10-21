#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单文件项目结构生成器

用法：
    1. 把本文件放到项目根目录
    2. 按需修改下面的配置
    3. python gen_tree.py
    4. 不要把脚本内容分成多个文件，因为写这个脚本的目的就是为了复制之后用完就走，分成多个文件不方便复制
"""

import fnmatch
import os
import unicodedata

# ============================ 配置区 ============================
# 目录/文件均支持通配符：* 任意字符，? 单字符，[abc] 字符集
IGNORE_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'node_modules',
    '.idea', '.vscode', 'photos',
    '*v',          # 忽略所有以 v 结尾的文件夹，不需要可删
}

IGNORE_FILES = {
    '.gitignore', '.DS_Store', 'gen_tree.py', '备忘录.txt',
    '*.jpg',       # 忽略所有 jpg 图片，不需要可删
}

OUTPUT_FILE = '项目结构.md'
MAX_DEPTH = -1     # -1 递归到底；1 只看根目录一层
SHOW_NOTES = True  # 是否在文件后显示首行备注
# ===============================================================


# ---------------------------- 通配符匹配 ----------------------------
def match_any(name, patterns):
    """名字是否命中任意一个通配符模式；无通配符时等价于字符串相等。"""
    return any(fnmatch.fnmatchcase(name, pattern) for pattern in patterns)


# ---------------------------- 显示宽度 ----------------------------
def display_width(text):
    """按“东亚宽字符占 2 列”计算显示宽度，用于中文对齐。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1
               for ch in text)


# ---------------------------- 首行备注 ----------------------------
# 不同扩展名允许的注释前缀（顺序即匹配优先级，长前缀最好在前）
_EXT_COMMENT_PREFIXES = {
    # 井号系
    '.py':      ('#', "'''", '"""'),
    '.pyi':     ('#', "'''", '"""'),
    '.pyw':     ('#', "'''", '"""'),
    '.sh':      ('#',),
    '.bash':    ('#',),
    '.zsh':     ('#',),
    '.fish':    ('#',),
    '.yml':     ('#',),
    '.yaml':    ('#',),
    '.toml':    ('#',),
    '.cfg':     ('#', ';'),
    '.ini':     ('#', ';'),
    '.conf':    ('#', ';'),
    '.env':     ('#',),
    '.rb':      ('#',),
    '.pl':      ('#',),
    '.r':       ('#',),
    '.jl':      ('#',),
    '.txt':     ('#', '//', '<!--'),
    # 双斜线系
    '.js':      ('//', '/*', '<!--'),
    '.mjs':     ('//', '/*', '<!--'),
    '.cjs':     ('//', '/*', '<!--'),
    '.jsx':     ('//', '/*', '<!--'),
    '.ts':      ('//', '/*', '<!--'),
    '.tsx':     ('//', '/*', '<!--'),
    '.java':    ('//', '/*'),
    '.c':       ('//', '/*'),
    '.h':       ('//', '/*'),
    '.cc':      ('//', '/*'),
    '.cpp':     ('//', '/*'),
    '.hpp':     ('//', '/*'),
    '.cs':      ('//', '/*'),
    '.go':      ('//', '/*'),
    '.rs':      ('//', '/*'),
    '.swift':   ('//', '/*'),
    '.kt':      ('//', '/*'),
    '.scala':   ('//', '/*'),
    '.dart':    ('//', '/*'),
    '.php':     ('//', '/*', '#'),
    '.css':     ('/*',),
    '.scss':    ('//', '/*'),
    '.less':    ('//', '/*'),
    '.proto':   ('//', '/*'),
    # 双横线系
    '.sql':     ('--',),
    '.lua':     ('--',),
    '.hs':      ('--',),
    '.elm':     ('--',),
    # HTML / XML 系
    '.html':    ('<!--',),
    '.htm':     ('<!--',),
    '.xml':     ('<!--',),
    '.svg':     ('<!--',),
    '.vue':     ('<!--', '//', '/*'),
    '.svelte':  ('<!--', '//', '/*'),
    '.md':      ('<!--',),      # 只认 HTML 注释，避免把 "# 标题" 当备注
    '.markdown': ('<!--',),
    # 明确不识别
    '.rst':     (),
    '.json':    (),
    '.csv':     (),
    '.log':     (),
}

# 行尾可能出现的成对闭合符
_CLOSERS = ('-->', '*/', "'''", '"""')


def _decode(raw):
    """逐行解码，先 UTF-8(带 BOM)，再兼容 GBK 系。"""
    for encoding in ('utf-8-sig', 'gb18030'):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def _strip_comment(text, prefixes):
    """命中注释前缀则返回纯备注文本，否则返回 None。"""
    for prefix in prefixes:
        if not text.startswith(prefix):
            continue
        body = text[len(prefix):].strip()
        for closer in _CLOSERS:
            if body.endswith(closer):
                body = body[:-len(closer)].strip()
                break
        body = body.lstrip('*').strip()      # /** 备注 */ 之类
        return body or None
    return None


def read_first_line_note(path, filename=None):
    """读取文本文件首个有效行的注释；不是注释或非文本返回 None。"""
    filename = filename or os.path.basename(path)
    prefixes = _EXT_COMMENT_PREFIXES.get(os.path.splitext(filename)[1].lower())
    if not prefixes:
        return None

    try:
        if os.path.getsize(path) > 1024 * 1024:      # 1MB 以上不读
            return None
        with open(path, 'rb') as f:
            for _ in range(5):                       # 最多试探前 5 行
                raw = f.readline()
                if not raw:
                    return None
                if b'\x00' in raw:                   # 二进制文件
                    return None
                line = _decode(raw)
                if line is None:
                    return None
                line = line.strip()
                if not line or line.startswith('#!'): # 空行 / shebang 跳过
                    continue
                return _strip_comment(line, prefixes)
    except OSError:
        return None
    return None


# ---------------------------- 目录树生成 ----------------------------
def generate_project_tree(root_dir, ignore_dirs=(), ignore_files=(),
                          max_depth=-1, show_notes=True):
    """生成项目目录树的 Markdown 代码块文本。"""
    rows = []       # [(所属目录, 行文本, 备注)]

    def walk(path, prefix="", depth=0):
        try:
            names = os.listdir(path)
        except OSError:
            return

        # 文件夹在前，文件在后
        items = sorted(
            names,
            key=lambda x: (0 if os.path.isdir(os.path.join(path, x)) else 1, x),
        )

        # 通配符过滤
        filtered = []
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                if match_any(item, ignore_dirs):
                    continue
            elif match_any(item, ignore_files):
                continue
            filtered.append(item)

        total = len(filtered)
        for index, item in enumerate(filtered):
            item_path = os.path.join(path, item)
            is_last = index == total - 1
            branch = "└── " if is_last else "├── "
            is_dir = os.path.isdir(item_path)

            note = None
            if show_notes and not is_dir:
                note = read_first_line_note(item_path, item)

            rows.append((path, f"{prefix}{branch}{item}", note))

            if is_dir and (max_depth == -1 or depth + 1 < max_depth):
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(item_path, new_prefix, depth + 1)

    root_name = os.path.basename(root_dir.rstrip(os.sep)) or root_dir
    rows.append((None, f"{root_name}/", None))
    rows.append((None, "│", None))
    walk(root_dir)

    # 每个目录内部单独对齐备注列
    widths = {}
    for group, text, note in rows:
        if note:
            widths[group] = max(widths.get(group, 0), display_width(text))

    lines = ["```"]
    for group, text, note in rows:
        if note:
            gap = widths[group] - display_width(text) + 2
            lines.append(f"{text}{' ' * gap}#{note}")
        else:
            lines.append(text)
    lines.append("```")
    return "\n".join(lines)


# ---------------------------- 入口 ----------------------------
if __name__ == "__main__":
    current_dir = os.getcwd()
    print("正在生成项目结构...\n")

    tree_text = generate_project_tree(
        current_dir,
        ignore_dirs=IGNORE_DIRS,
        ignore_files=IGNORE_FILES,
        max_depth=MAX_DEPTH,
        show_notes=SHOW_NOTES,
    )
    print(tree_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(tree_text)

    print(f"\n项目结构已保存到：{OUTPUT_FILE}")
