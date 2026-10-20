import os

# 要忽略的文件夹
IGNORE_DIRS = {'__pycache__', '.git', '.venv', 'venv', 'node_modules', '.idea', '.vscode', 'photos'}
# 要忽略的文件
IGNORE_FILES = {'.gitignore', '.DS_Store', 'gene.py', '备忘录.txt'}
# 输出文件名
OUTPUT_FILE = '项目结构.md'
# 递归深度：-1 表示不限制（递归到底），正整数表示最大递归层数
# 根目录算作第 0 层；MAX_DEPTH=1 时只列出根目录下的直接文件和文件夹，不展开子文件夹
MAX_DEPTH = -1


def generate_project_tree(root_dir):
    tree_lines = []
    tree_lines.append("```")
    root_name = os.path.basename(root_dir.rstrip(os.sep)) or root_dir
    tree_lines.append(f"{root_name}/")
    tree_lines.append("│")

    def walk(path, prefix="", depth=0):
        # 列出内容：文件夹在前，文件在后
        items = sorted(os.listdir(path))
        items.sort(key=lambda x: (0 if os.path.isdir(os.path.join(path, x)) else 1, x))
        # 过滤忽略项
        items = [
            item for item in items
            if not (os.path.isdir(os.path.join(path, item)) and item in IGNORE_DIRS)
            and not (os.path.isfile(os.path.join(path, item)) and item in IGNORE_FILES)
        ]
        total = len(items)
        for index, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = index == total - 1
            is_dir = os.path.isdir(item_path)
            # 绘制符号
            branch = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{branch}{item}")
            # 递归子文件夹：受 MAX_DEPTH 控制
            if is_dir and (MAX_DEPTH == -1 or depth + 1 < MAX_DEPTH):
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(item_path, new_prefix, depth + 1)

    walk(root_dir, prefix="", depth=0)
    tree_lines.append("```")
    return "\n".join(tree_lines)


if __name__ == "__main__":
    current_dir = os.getcwd()
    print("正在生成项目结构...\n")

    tree_text = generate_project_tree(current_dir)
    print(tree_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(tree_text)

    print(f"\n项目结构已保存到：{OUTPUT_FILE}")
