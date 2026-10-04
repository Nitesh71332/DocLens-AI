# DocuLens AI

### Evidence-First Intelligent Document Investigator

DocuLens AI is an intelligent document investigation platform that allows users to upload multiple documents, ask natural-language questions, retrieve supporting evidence, compare information across sources, detect conflicts, and communicate uncertainty instead of confidently guessing.

Built for **ALGOTHON'26 — PS ALG-AI-02: Intelligent Document Investigator**.

---

## Problem

Important information is often distributed across multiple documents such as:

- Employee handbooks
- HR policies
- Contracts
- Reports
- PDFs
- Word documents
- Text files
- Scanned documents and images

Traditional document search forces users to manually inspect every file.

A normal RAG system can also produce a single confident answer even when two documents disagree.

DocuLens AI is designed to solve this problem by treating document question answering as an **investigation** rather than simple retrieval.

Instead of only asking:

> "What does the model think the answer is?"

DocuLens asks:

> "What evidence do the documents provide, do the sources agree, and can the answer actually be verified?"

---

## Key Features

### 1. Multi-document investigation

Upload multiple documents and investigate information across the complete document collection.

Supported formats:

- PDF
- DOCX
- TXT
- PNG
- JPG / JPEG

---

### 2. Text extraction and OCR

DocuLens extracts text from uploaded documents.

For image-based or scanned content, OCR is used to extract readable text before indexing.

The system preserves document and page information so retrieved evidence can be traced back to its source.

---

### 3. Hybrid retrieval

DocuLens combines:

- Vector similarity search
- BM25 keyword retrieval

This allows the system to handle both semantic questions and exact information such as:

- Names
- Numbers
- Dates
- Amounts
- Policy values

The retrieved passages are then passed through the investigation pipeline.

---

### 4. Evidence-grounded answers

Every supported answer can include:

- Source filename
- Page number
- Section
- Direct supporting quote
- Evidence strength
- Investigation trace

Citations are verified against the indexed source text before being presented as verified evidence.

---

### 5. Conflict detection

DocuLens compares information across documents and identifies cases where different documents provide different values for the same fact.

For example:

```text
Company Policy
Remote work: 3 days per week

HR Update
Remote work: 2 days per week