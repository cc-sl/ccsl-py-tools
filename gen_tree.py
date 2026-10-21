# 生成项目结构入口
import os
from core.tree import generate_project_tree

IGNORE_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'node_modules',
    '.idea', '.vscode', 'photos',
    '*v',
}
IGNORE_FILES = {
    '.gitignore', '.DS_Store', 'gen_tree.py', '备忘录.txt',
    '*.jpg',
}
OUTPUT_FILE = '项目结构.md'
MAX_DEPTH = -1
SHOW_NOTES = True

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
