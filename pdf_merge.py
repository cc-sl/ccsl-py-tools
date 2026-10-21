from core.pdf import merge_pdfs
# 按顺序写你的 pdf，顺序就是合并顺序
PDF_FILES = ["b.pdf", "a.pdf"]
OUTPUT_FILE = "合并结果.pdf"

if __name__ == "__main__":
    merge_pdfs(PDF_FILES, OUTPUT_FILE)
    print("合并完成")
