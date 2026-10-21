"""生成项目目录树的 Markdown 代码块文本。"""

import os

from .matcher import match_any
from .notes import read_first_line_note
from .textwidth import display_width


def generate_project_tree(root_dir, ignore_dirs=(), ignore_files=(),
                          max_depth=-1, show_notes=True):
    """生成项目目录树的 Markdown 代码块文本。

    show_notes=True 时，文本文件首行若是注释，会在文件名后追加 `#备注`。
    """
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
