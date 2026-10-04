import pymupdf

doc=pymupdf.open()

page=doc.new_page()

text="""DocuLens AI Test Document

Employee Name: Rahul Kumar

The annual salary is ₹8,40,000.

The probation period is 6 months.

This document is used to test document extraction."""

page.insert_text((72,72),text,fontsize=12)

doc.save("../sample_documents/test_document.pdf")
doc.close()

print("PDF created successfully")