import re

def remove_markdown(text):
    """把 Markdown 文本转成纯文本（保留可见内容，去掉标记）。"""
    # 先移除代码块，避免块内符号被后续规则误处理
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # 移除图片标记（必须在链接之前，否则会残留 "!"）
    text = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', text)

    # 移除链接标记
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)

    # 移除粗体标记
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)

    # 移除斜体标记
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)

    # 移除内联代码标记
    text = re.sub(r'`(.*?)`', r'\1', text)

    # 移除标题标记
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)

    # 移除引用标记
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)

    # 移除水平分割线
    text = re.sub(r'^[-*]{3,}\s*$', '', text, flags=re.MULTILINE)

    # 移除无序列表标记
    text = re.sub(r'^(\s*)[-*+]\s+', r'\1', text, flags=re.MULTILINE)

    # 移除有序列表标记
    text = re.sub(r'^(\s*)\d+\.\s+', r'\1', text, flags=re.MULTILINE)

    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    return text.strip()
