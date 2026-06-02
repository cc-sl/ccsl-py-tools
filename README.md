# Gene - 项目结构生成器

一个简洁的 Python 脚本，自动扫描当前目录并生成美观的项目结构树状图，输出为 Markdown 格式文件。

## 功能

- 递归扫描当前目录下的所有文件和文件夹
- 使用 Unicode 树状字符（`├──`、`└──`、`│`）绘制结构图
- 自动忽略常见无关目录（`__pycache__`、`.git`、`node_modules` 等）
- 输出为 Markdown 代码块，可直接嵌入文档

## 使用方法

```bash
python gene.py
```

运行后会在当前目录生成 `项目结构.md` 文件，内容为一个 Markdown 代码块，展示目录树结构。

## 自定义忽略项

编辑 `gene.py` 中的以下变量即可：

```python
# 要忽略的文件夹
IGNORE_DIRS = {'__pycache__', '.git', '.venv', 'venv', 'node_modules', '.idea', '.vscode', 'photos'}

# 要忽略的文件
IGNORE_FILES = {'.gitignore', '.DS_Store', 'gene.py', '备忘录.txt'}
```

## 示例输出

    gene/
    │
    ├── 示例结构
    │   ├── 二层文件夹
    │   │   └── 二层脚本.py
    │   ├── 实例文件.js
    │   ├── 实例文件.py
    │   └── 示例文件.cpp
    └── 项目结构.md

## 环境要求

- Python 3.6+

## 开源协议

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
