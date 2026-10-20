import re
import pyperclip

def remove_markdown(text):
    # 移除图片标记
    text = re.sub(r'!$$(.*?)$$$.*?$', r'\1', text)
    
    # 移除链接标记
    text = re.sub(r'$$(.*?)$$$.*?$', r'\1', text)
    
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
    
    # 移除代码块标记
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    
    return text.strip()

def main():
    print("请输入文本（以单独一行'E'结束输入）：")
    lines = []
    while True:
        line = input()
        if line.strip() == 'E':
            break
        lines.append(line)
    
    input_text = '\n'.join(lines)
    cleaned_text = remove_markdown(input_text)
    
    print("\n去除Markdown后的文本：")
    print(cleaned_text)
    pyperclip.copy(cleaned_text)
    print('已经写入剪切板，CTRL+V进行粘贴')
    print()


if __name__ == "__main__":
    while True:
        main()
