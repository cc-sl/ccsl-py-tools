# 按列表顺序合并 PDF 并写入 output_file
from pypdf import PdfReader, PdfWriter


def merge_pdfs(pdf_files, output_file):
    """按列表顺序合并 PDF 并写入 output_file。"""
    pdf_files = list(pdf_files)
    if not pdf_files:
        raise ValueError("没有可合并的 PDF 文件")

    writer = PdfWriter()
    for path in pdf_files:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)
