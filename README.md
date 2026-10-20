
# ccsl-py-tools

> Python 小工具集，包含 PDF合并、项目目录树生成、Markdown去除标记工具

## 功能介绍

1. **PDF合并脚本（pdf_merge.py）**

   - 功能：按自定义顺序批量合并多个PDF文件
   - 使用方法：
     1. 修改代码中 `pdf_files` 列表，填写需要合并的PDF文件名，**列表顺序即为PDF合并后的页码顺序**
     2. 将待合并PDF文件放在脚本同目录下
     3. 运行脚本，自动生成 `合并结果.pdf`
   - 依赖：`pypdf`
2. **项目结构树生成脚本（gen_tree.py）**

   - 功能：自动扫描当前项目目录，生成Markdown格式的项目目录树，输出 `项目结构.md`
   - 可配置项（脚本顶部）：
     - `IGNORE_DIRS`：需要忽略扫描的文件夹
     - `IGNORE_FILES`：需要忽略扫描的文件
     - `MAX_DEPTH`：目录递归深度，`-1` 无限制，最小为1
     - `OUTPUT_FILE`：输出md文件名称
   - 使用方法：直接运行脚本，会自动打印目录树并保存为markdown文件
3. **Markdown标记去除脚本（remove_md.py）**

   - 功能：清除文本里的 Markdown 语法标记，保留纯文本，处理完成自动复制结果到剪贴板
   - 可清理内容：图片、超链接、粗体、斜体、行内代码、标题、引用、分割线、有序/无序列表、代码块、HTML标签
   - 使用方法：
     1. 运行脚本，逐行粘贴输入文本
     2. 在单独一行输入 `E` 结束输入
     3. 程序输出纯文本，并自动复制到剪贴板，直接 Ctrl+V 粘贴
   - 依赖：`pyperclip`

## 使用步骤

1. 安装依赖包

```bash
pip install pypdf pyperclip
```

2. 按需修改对应脚本内配置
3. 执行脚本

```bash
# PDF合并
python pdf_merge.py

# 生成项目结构树
python gen_tree.py

# 去除Markdown标记
python remove_md.py
```

## 文件说明

```
├── pdf_merge.py        # PDF合并脚本
├── gen_tree.py         # 项目结构树生成脚本
├── remove_md.py        # Markdown标记去除脚本
├── README.md           # 项目说明文档
├── a.pdf               # 待合并PDF示例
├── b.pdf               # 待合并PDF示例
└── 合并结果.pdf        # PDF合并输出文件
```

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

---

> `pyperclip` 在Linux环境可能需要额外安装系统剪贴板依赖（如`xclip`），Windows/macOS一般直接可用。
