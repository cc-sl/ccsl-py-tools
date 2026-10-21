
2. 按需修改对应入口脚本顶部的“配置区”
3. 执行脚本

# ccsl-py-tools

> Python 小工具集，包含 PDF 合并、项目目录树生成、Markdown 去除标记工具

## 功能介绍

1. **PDF 合并脚本（pdf_merge.py）**

   - 功能：按自定义顺序批量合并多个 PDF 文件
   - 使用方法：
     1. 修改脚本顶部配置区的 `PDF_FILES` 列表，填写需要合并的 PDF 文件名，**列表顺序即为 PDF 合并后的页码顺序**
     2. 将待合并 PDF 文件放在脚本同目录下
     3. 运行脚本，自动生成 `合并结果.pdf`
   - 依赖：`pypdf`
2. **项目结构树生成脚本（gen_tree.py）**

   - 功能：自动扫描当前项目目录，生成 Markdown 格式的项目目录树，输出 `项目结构.md`
   - 可配置项（脚本顶部）：
     - `IGNORE_DIRS`：需要忽略扫描的文件夹，支持通配符
     - `IGNORE_FILES`：需要忽略扫描的文件，支持通配符
     - `MAX_DEPTH`：目录递归深度，`-1` 无限制，最小为 1
     - `OUTPUT_FILE`：输出 md 文件名称
   - 通配符规则（基于 `fnmatch`）：
     - `*.jpg` → 忽略所有 jpg 文件
     - `*v` → 忽略所有以 v 结尾的文件夹
     - 不带通配符的名字 → 精确匹配，如 `__pycache__`
   - 使用方法：直接运行脚本，会自动打印目录树并保存为 markdown 文件
3. **Markdown 标记去除脚本（remove_md.py）**

   - 功能：清除文本里的 Markdown 语法标记，保留纯文本，处理完成自动复制结果到剪贴板
   - 可清理内容：图片、超链接、粗体、斜体、行内代码、标题、引用、分割线、有序/无序列表、代码块、HTML 标签
   - 使用方法：
     1. 运行脚本，逐行粘贴输入文本
     2. 在单独一行输入 `E` 结束输入
     3. 程序输出纯文本，并自动复制到剪贴板，直接 Ctrl+V 粘贴
   - 依赖：`pyperclip`

## 使用步骤

1. 安装依赖包

```bash
pip install -r requirements.txt
```
2. 按需修改对应入口脚本顶部的“配置区”

3. 执行脚本

```bash
# PDF合并
python pdf_merge.py

# 生成项目结构树
python gen_tree.py

# 去除Markdown标记
python remove_md.py
```
## 项目结构
三个入口脚本保留在根目录，所有实际逻辑放在 core/ 下，一个功能一个文件，方便单独维护。

```bash
├── pdf_merge.py        # 入口：PDF合并
├── gen_tree.py         # 入口：项目结构树生成
├── remove_md.py        # 入口：Markdown标记去除
├── requirements.txt    # 依赖清单
├── README.md           # 项目说明文档
│
├── core/
│   ├── __init__.py     # 包标识，保持为空
│   ├── matcher.py      # 通配符匹配（*.jpg / *v 等）
│   ├── tree.py         # 目录树生成算法
│   ├── pdf.py          # PDF合并算法
│   └── markdown.py     # Markdown去标记算法
│
├── a.pdf               # 待合并PDF示例
├── b.pdf               # 待合并PDF示例
├── 合并结果.pdf         # PDF合并输出文件
└── 项目结构.md          # 目录树输出文件
```

## 环境要求
Python 3.6+

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
