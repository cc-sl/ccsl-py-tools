# 合并pdf入口
from pathlib import Path

from core.pdf import merge_pdfs

# PDF 所在文件夹（以脚本所在目录为基准，任意位置运行都正确）
PDF_DIR = Path(__file__).resolve().parent / "thepdf"
OUTPUT_FILE = Path(__file__).resolve().parent / "合并结果.pdf"

if __name__ == "__main__":
    # 取出 thepdf 下所有 pdf，按文件名排序，数量不限
    pdf_files = sorted(PDF_DIR.glob("*.pdf"), key=lambda p: p.name)

    if not pdf_files:
        print(f"{PDF_DIR} 中没有找到 PDF 文件")
    else:
        print("合并顺序：")
        for p in pdf_files:
            print(f"  - {p.name}")

        merge_pdfs([str(p) for p in pdf_files], str(OUTPUT_FILE))
        print(f"合并完成 -> {OUTPUT_FILE}")
