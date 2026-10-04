from PIL import Image,ImageDraw,ImageFont

image=Image.new("RGB",(1000,600),"white")
draw=ImageDraw.Draw(image)

font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf",32)

text="""DocuLens AI OCR Test

Employee Name: Rahul Kumar

Annual Salary: ₹8,40,000

Probation Period: 6 months"""

draw.multiline_text((50,50),text,fill="black",font=font,spacing=20)

image.save("../sample_documents/test_ocr.png")

print("OCR test image created successfully")