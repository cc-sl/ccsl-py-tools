# 移除md标记入口
import pyperclip

from core.markdown import remove_markdown


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
