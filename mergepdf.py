
from pypdf import PdfReader, PdfWriter

writer = PdfWriter()

# 按这里写你的pdf，顺序就是合并顺序
pdf_files = ["b.pdf", "a.pdf"]

for path in pdf_files:
    reader = PdfReader(path)
    for page in reader.pages:
        writer.add_page(page)

# 输出合并后的文件
with open("合并结果.pdf", "wb") as f:
    writer.write(f)

print("合并完成")