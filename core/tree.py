import os
from .matcher import match_any

def generate_project_tree(root_dir, ignore_dirs=(), ignore_files=(), max_depth=-1):
    """生成项目目录树的 Markdown 代码块文本。"""
    tree_lines = ["```"]
    root_name = os.path.basename(root_dir.rstrip(os.sep)) or root_dir
    tree_lines.append(f"{root_name}/")
    tree_lines.append("│")

    def walk(path, prefix="", depth=0):
        # 文件夹在前，文件在后
        items = sorted(
            os.listdir(path),
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
            tree_lines.append(f"{prefix}{branch}{item}")

            if os.path.isdir(item_path) and (max_depth == -1 or depth + 1 < max_depth):
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(item_path, new_prefix, depth + 1)

    walk(root_dir)
    tree_lines.append("```")
    return "\n".join(tree_lines)
