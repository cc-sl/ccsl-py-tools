import os

# 要忽略的文件夹
IGNORE_DIRS = {'__pycache__', '.git', '.venv', 'venv', 'node_modules', '.idea', '.vscode','photos'}
# 要忽略的文件
IGNORE_FILES = {'.gitignore', '.DS_Store', 'gene.py','备忘录.txt'}
# 输出文件名
OUTPUT_FILE = '项目结构.md'

def generate_project_tree(root_dir):
    tree_lines = []
    root_name = os.path.basename(root_dir)
    tree_lines.append(f"{root_name}/")
    tree_lines.append("│")

    def walk(path, prefix="", is_root=False):
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

            # 递归子文件夹
            if is_dir:
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk(item_path, new_prefix)

        # 根目录：模块之间加空行
        if is_root and total > 0 and not is_last:
            tree_lines.append(f"{prefix}│")

    walk(current_dir, prefix="", is_root=True)
    return "\n".join(tree_lines)

if __name__ == "__main__":
    current_dir = os.getcwd()
    print("正在生成项目结构...\n")
    
    tree_text = generate_project_tree(current_dir)
    print(tree_text)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(tree_text)
    
    print(f"\n项目结构已保存到：{OUTPUT_FILE}")