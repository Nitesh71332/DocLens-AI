from app.ingestion.extractors import extract_document

path="../sample_documents/test_document.txt"

pages=extract_document(path)

for page in pages:
    print("PAGE:",page["page"])
    print(page["text"])