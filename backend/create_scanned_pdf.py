import pymupdf

image_path="../sample_documents/test_ocr.png"
output_path="../sample_documents/test_scanned.pdf"

image_doc=pymupdf.open()
page=image_doc.new_page(width=595,height=842)

page.insert_image(
    page.rect,
    filename=image_path
)

image_doc.save(output_path)
image_doc.close()

print("Scanned PDF created successfully")