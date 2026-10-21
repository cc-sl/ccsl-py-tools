import os
from core.tree import generate_project_tree
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

if __name__ == "__main__":
    current_dir = os.getcwd()
    print("正在生成项目结构...\n")

    tree_text = generate_project_tree(
        current_dir,
        ignore_dirs=IGNORE_DIRS,
        ignore_files=IGNORE_FILES,
        max_depth=MAX_DEPTH,
    )
    print(tree_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(tree_text)

    print(f"\n项目结构已保存到：{OUTPUT_FILE}")
