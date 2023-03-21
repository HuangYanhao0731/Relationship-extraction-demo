import fitz # PyMuPDF库

# 打开PDF文件
pdf_document = "Data/A27_260-292.pdf"
doc = fitz.open(pdf_document)

# 遍历PDF的每一页
for page in doc:
    zoom_x = 2.0  # horizontal zoom
    zomm_y = 2.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zomm_y)  # zoom factor 2 in each dimension
    # 将每一页保存为PNG图片
    pix = page.get_pixmap(matrix=mat)
    output_file = f"output/ninth/page_{page.number}.png"
    pix.save(output_file)

# 关闭PDF文件
doc.close()
