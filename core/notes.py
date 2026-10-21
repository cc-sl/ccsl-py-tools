"""读取文本文件首行注释，作为项目结构的备注。"""

import os

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
    """读取文本文件首个有效行的注释；不是注释或非文本返回 None。

    - 按扩展名决定“什么算注释”，避免误判
    - 含 NUL 字节视为二进制，直接跳过
    - 跳过空行和 shebang（#!...）
    - 首行注释形如 #、//、--、'''、\"""、<!--、/*、; 等
    """
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
