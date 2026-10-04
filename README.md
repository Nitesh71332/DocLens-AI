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

Loading older messages…
Give me final README
Absolutely, Captain. Below is the complete final README.md. Replace everything currently inside your README.md with this entire content.

# DocuLens AI

## Evidence-First Intelligent Document Investigator

**ALGOTHON'26 — PS ALG-AI-02: Intelligent Document Investigator**

DocuLens AI is an intelligent document investigation platform that allows users to upload multiple documents, ask natural-language questions, retrieve supporting evidence, compare information across sources, detect conflicts, and communicate uncertainty instead of confidently guessing.

The system treats document question answering as an **investigation problem**, not simply a retrieval problem.

Instead of asking only:

> "What does the model think the answer is?"

DocuLens asks:

> "What evidence do the documents provide, do the sources agree, and can the answer actually be verified?"

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Investigation Verdicts](#investigation-verdicts)
- [Evidence Strength](#evidence-strength)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Local Setup](#local-setup)
- [Example Investigation](#example-investigation)
- [Conflict Detection](#conflict-detection)
- [Testing and Edge Cases](#testing-and-edge-cases)
- [ALG-AI-02 Requirement Mapping](#alg-ai-02-requirement-mapping)
- [Reliability Principles](#reliability-principles)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [External APIs and AI Disclosure](#external-apis-and-ai-disclosure)
- [Project Status](#project-status)
- [Repository](#repository)
- [Author](#author)

---

## Problem Statement

Important information is often distributed across multiple documents such as:

- Employee handbooks
- HR policies
- Contracts
- Reports
- PDFs
- Word documents
- Text files
- Scanned documents
- Images

Traditional document search forces users to manually inspect every file.

A conventional RAG system can also produce a single confident answer even when two documents disagree.

This creates an important problem:

**What happens when the retrieved sources contradict each other?**

DocuLens AI addresses this by treating document question answering as an evidence investigation workflow.

The system retrieves relevant passages, compares claims across documents, verifies supporting citations, detects conflicts, and assigns an investigation verdict.

---

## Solution

DocuLens AI provides an evidence-first workflow:

```text
Multiple Documents
        |
        v
Document Extraction / OCR
        |
        v
Chunking and Indexing
        |
        v
Hybrid Retrieval
(Vector + BM25)
        |
        v
Relevant Evidence
        |
        v
Claim Comparison
        |
        v
Conflict Detection
        |
        v
Citation Verification
        |
        v
Evidence Strength
        |
        v
Investigation Verdict
The system avoids blindly trusting a single generated answer.

If evidence is insufficient, the system can return:

NOT_FOUND
If sources disagree, the system can return:

CONFLICT
If the evidence supports a newer or authoritative value, the system can identify:

SUPERSEDED
Key Features
1. Multi-document Investigation
Users can upload multiple documents and investigate information across the complete document collection.

Supported formats:

PDF
DOCX
TXT
PNG
JPG
JPEG
2. Text Extraction and OCR
DocuLens extracts text from uploaded documents.

For image-based or scanned content, OCR is used to extract readable text before indexing.

Document metadata such as filename, page number, and section information is preserved so retrieved evidence can be traced back to the original source.

3. Hybrid Retrieval
DocuLens combines two retrieval approaches:

Vector similarity search
BM25 keyword retrieval
Vector retrieval helps identify semantically related passages.

BM25 helps with exact terms and structured information such as:

Names
Numbers
Dates
Amounts
Policy values
Identifiers
The combination provides more robust retrieval than relying on only one search strategy.

4. Evidence-Grounded Answers
Supported answers can include:

Source filename
Page number
Section
Direct supporting quote
Evidence strength
Investigation trace
Citations are verified against the indexed source text before being presented as verified evidence.

5. Conflict Detection
DocuLens compares claims across multiple documents.

For example:

Company Policy
Remote work: 3 days per week

HR Update
Remote work: 2 days per week
Instead of silently selecting one value, DocuLens can identify the disagreement and surface the competing claims.

The Conflict Center provides a dedicated view for examining detected conflicts.

6. Uncertainty Handling
DocuLens does not assume that every question has an answer.

When supporting evidence is insufficient, the system communicates uncertainty instead of presenting an unsupported answer as fact.

The investigation engine uses five main verdicts:

CONFIRMED
CONFLICT
SUPERSEDED
UNCERTAIN
NOT_FOUND
7. Citation Verification
Generated answers are not treated as evidence by themselves.

DocuLens checks whether the supporting quote exists in the indexed document text.

This helps reduce unsupported citations and hallucinated references.

8. Investigation Trace
The interface can expose the investigation process through a trace.

A typical investigation follows:

Retrieve passages
        ↓
Apply relevance filtering
        ↓
Compare claims
        ↓
Analyze conflicts
        ↓
Verify citations
        ↓
Calculate evidence strength
        ↓
Generate final verdict
This makes the result more explainable to the user.

How It Works
Step 1 — Upload
The user uploads one or more supported documents.

PDF
DOCX
TXT
PNG
JPG / JPEG
Step 2 — Extract
The backend extracts text from the uploaded documents.

For scanned or image-based documents, OCR is used.

Step 3 — Chunk
Extracted content is divided into smaller passages.

Each passage maintains metadata such as:

Document
Page
Section
Chunk ID
OCR information when applicable
Step 4 — Index
The extracted passages are indexed for retrieval.

DocuLens uses:

Chroma for vector retrieval
BM25 for keyword retrieval
SQLite for application metadata
Step 5 — Investigate
The user asks a natural-language question.

Example:

What is Rahul Kumar's annual salary?
Step 6 — Retrieve Evidence
Relevant passages are retrieved from the indexed documents.

The system applies a relevance gate before using passages as supporting evidence.

Step 7 — Compare Claims
The investigation engine compares relevant claims across the retrieved documents.

This allows the system to identify situations where multiple documents provide different values.

Step 8 — Verify
Supporting citations are checked against the indexed source text.

Only verified source quotes are presented as verified evidence.

Step 9 — Generate Verdict
The system returns an investigation result containing:

Answer
Verdict
Reason
Evidence score
Evidence strength
Citations
Conflict information
Investigation trace
Investigation Verdicts
Verdict	Meaning
CONFIRMED	Supporting evidence is sufficient and verified
CONFLICT	Multiple sources provide conflicting claims
SUPERSEDED	A newer or more authoritative value can be identified
UNCERTAIN	Some evidence exists, but it is not sufficient for a reliable conclusion
NOT_FOUND	The indexed documents do not contain enough information to answer the question
The verdict is intentionally separate from the generated answer.

This allows the system to communicate how reliable the investigation result is, rather than simply displaying generated text.

Evidence Strength
DocuLens uses an evidence score on a scale of:

0 - 100
The system also reports an evidence-strength category such as:

STRONG
MODERATE
WEAK
NONE
The evidence score is a heuristic evidence score.

It is:

Not a probability
Not a statistical confidence interval
Not a guarantee of correctness
The purpose is to communicate the strength of the available supporting evidence.

Architecture
DocuLens AI follows an evidence-first architecture combining document processing, hybrid retrieval, LLM reasoning, citation verification, and conflict detection.



Major Components
Frontend
The React frontend provides:

Document upload
Investigation interface
Evidence display
Investigation results
Conflict Center
Investigation trace
Backend
FastAPI provides the application API and coordinates:

Document processing
Retrieval
Investigation
Citation verification
Conflict analysis
Database operations
Document Processing
The ingestion pipeline handles supported document formats and OCR processing.

Retrieval
The retrieval layer combines:

Vector similarity
BM25 keyword retrieval
Investigation Engine
The investigation layer analyzes retrieved evidence and produces:

Answer
Verdict
Reason
Evidence strength
Citations
Conflict information
Storage
SQLite stores application metadata.

Chroma stores vector-indexed document chunks.

Technology Stack
Frontend
React
Vite
JavaScript
CSS
Lucide React
Backend
Python
FastAPI
Uvicorn
Document Processing
PyMuPDF
python-docx
RapidOCR
OpenCV
Retrieval
Chroma
BM25
Vector similarity search
Storage
SQLite
LLM
Google Gemini API
Project Structure
DocLens-AI/
│
├── backend/
│   ├── app/
│   ├── sample_documents/
│   └── test_documents/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── architecture.png
│
├── .gitignore
└── README.md
API Endpoints
Health Check
GET /api/health
Checks whether the backend is available.

List Documents
GET /api/documents
Returns uploaded document information and collection statistics.

Upload Document
POST /api/documents/upload
Uploads and processes a document.

The backend extracts text, performs OCR when necessary, chunks the content, and indexes it.

Delete Document
DELETE /api/documents/{doc_id}
Deletes a document from the collection.

Investigate Question
POST /api/investigate
Request:

{
  "question": "What is Rahul Kumar's annual salary?"
}

The response can contain:

Answer
Verdict
Reason
Evidence score
Evidence strength
Citations
Evidence
Conflict information
Investigation trace
Get Conflicts
GET /api/conflicts
Returns detected and possible conflicts across the indexed documents.

Local Setup
Prerequisites
Install:

Python 3.11
Node.js
npm
Git
1. Clone the Repository
git clone https://github.com/Nitesh71332/DocLens-AI.git
cd DocLens-AI

2. Activate the Python Environment
The project uses a Python virtual environment named .venv.

From the backend directory:

Windows PowerShell
cd backend
..\.venv\Scripts\activate

3. Configure Environment Variables
Create or configure:

backend/.env
Example:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
Do not commit API keys to GitHub.

The .env file is excluded through .gitignore.

4. Start the Backend
From the backend directory:

uvicorn app.main:app --reload --port 8000

Backend:

http://127.0.0.1:8000
5. Start the Frontend
Open another terminal:

cd frontend
npm install
npm run dev
Frontend:

http://localhost:5173
Example Investigation
Suppose the document contains:

Employee Handbook

Annual Salary:
The annual salary for Rahul Kumar is ₹8,40,000.
The user asks:

What is Rahul Kumar's annual salary?
DocuLens can return:

Answer:
Rahul Kumar's annual salary is ₹8,40,000.

Verdict:
CONFIRMED

Evidence:
employee_handbook.txt
Page 1
Section: Annual Salary

Quote:
"The annual salary for Rahul Kumar is ₹8,40,000."
The answer is supported by a directly verified source quote.

Conflict Detection
DocuLens is designed to identify disagreements between documents.

For example:

Employee Handbook

Probation Period:
6 months
and:

HR Policy

Probation Period:
3 months
Instead of silently choosing one value, DocuLens can identify:

CONFLICT
The Conflict Center can then show the competing claims and their respective source documents.

This is one of the core differences between a simple document Q&A system and an investigation-oriented system.

Testing and Edge Cases
DocuLens was tested against multiple investigation scenarios.

Test Scenario	Expected Behavior
Known salary question	CONFIRMED
Conflicting probation periods	CONFLICT
Unknown passport number	NOT_FOUND
Known working-hours question	CONFIRMED
Remote-work disagreement	Conflict detected by Conflict Center
Multiple uploaded documents	Cross-document retrieval
Image/scanned content	OCR processing
Unsupported question	No unsupported source-backed claim
Example Confirmed Result
Question:
What is Rahul Kumar's annual salary?

Verdict:
CONFIRMED

Evidence Score:
70 / 100

Evidence Strength:
MODERATE

Source:
employee_handbook.txt

Page:
1

Section:
Annual Salary
Example Not Found Result
Question:
What is the company's office address?

Verdict:
NOT_FOUND
The system does not invent an office address when supporting information is absent from the indexed documents.

Example Conflict
Company Policy
Remote work: 3 days per week

HR Update
Remote work: 2 days per week
The Conflict Center identifies the competing claims.

ALG-AI-02 Requirement Mapping
Problem Requirement	DocuLens Implementation
Multiple document formats	PDF, DOCX, TXT, PNG, JPG/JPEG
Document extraction	PyMuPDF and python-docx
OCR	RapidOCR/OpenCV
Document indexing	Chroma vector store + BM25
Natural-language Q&A	FastAPI investigation pipeline + LLM
Source references	Filename, page, section and direct quotes
Citation verification	Retrieved quote validation against source text
Conflict detection	Cross-document claim comparison
Uncertainty handling	CONFIRMED, CONFLICT, SUPERSEDED, UNCERTAIN, NOT_FOUND
Investigation workflow	Retrieve → Compare → Verify → Verdict
Usable investigation interface	React frontend + Evidence Panel + Conflict Center
Reliability Principles
DocuLens follows several principles to reduce unsupported answers.

1. Evidence before confidence
The system prioritizes source evidence instead of relying only on generated text.

2. No evidence means no confident answer
If supporting information cannot be found, the system can return:

NOT_FOUND
3. Conflicting evidence is surfaced
Different source claims are not silently merged into one answer.

4. Citations are verified
Supporting quotes are checked against indexed source content.

5. Uncertainty is explicit
The system distinguishes between confirmed, conflicting, superseded, uncertain, and unavailable information.

Limitations
Current limitations include:

OCR accuracy depends on image quality.
Very complex document layouts may not extract perfectly.
LLM availability and API quotas can affect investigation responses.
Evidence scoring is heuristic rather than probabilistic.
Conflict resolution may require stronger temporal and organizational reasoning for complex real-world policies.
The current system is primarily designed for document-grounded investigation rather than unrestricted web research.
Production deployment requires persistent storage configuration for SQLite and Chroma.
Future Improvements
Potential future improvements include:

Support for additional document formats
Better table extraction
Improved OCR for difficult scans
Advanced temporal reasoning
More sophisticated entity and claim extraction
Stronger authority and document-priority reasoning
Persistent cloud vector storage
Cloud database support
Authentication and role-based access
Multi-user workspaces
Document version tracking
Better conflict-resolution explanations
Larger-scale document collections
Production monitoring and observability
External APIs and AI Disclosure
DocuLens AI uses external AI capabilities as part of the investigation pipeline.

External API
Google Gemini API is used for language-model reasoning.

An API key is required through an environment variable.

API credentials are not stored in the repository.

AI-Assisted Development
AI-assisted development tools were used during implementation for activities such as:

Code generation
Debugging
UI development assistance
Documentation assistance
Architecture and implementation guidance
The final application, integration, testing, configuration, and validation were performed as part of the project development process.

Project Status
Completed
Multi-document upload
PDF support
DOCX support
TXT support
Image support
OCR pipeline
Document extraction
Document chunking
Vector indexing
BM25 retrieval
Hybrid retrieval
Natural-language investigation
Evidence citations
Citation verification
Evidence scoring
Conflict detection
Conflict Center
Uncertainty-aware verdicts
Investigation trace
React frontend
FastAPI backend
README documentation
Architecture diagram
GitHub repository
Planned
Production deployment
Larger-scale persistent storage
Advanced document version reasoning
Additional automated testing
Improved OCR and table extraction
Demo Workflow
For a demonstration, use the following sequence:

1. Upload multiple documents
Upload documents containing related information.

2. Ask a factual question
Example:

What is Rahul Kumar's annual salary?
Show:

Answer
Verdict
Evidence score
Source quote
3. Ask a conflicting question
Example:

What is the probation period?
Show the conflicting values across documents.

4. Open Conflict Center
Demonstrate the competing source claims.

5. Ask an unsupported question
Example:

What is the company's office address?
Show:

NOT_FOUND
This demonstrates that DocuLens does not simply hallucinate an answer.

Repository
GitHub:

https://github.com/Nitesh71332/DocLens-AI

Author
Nitesh Kumar

B.Tech — Computer Science and Engineering
Indian Institute of Information Technology Kottayam

ALGOTHON'26
PS ALG-AI-02 — Intelligent Document Investigator

AI may help build it. But the evidence still has to support the answer.


### After replacing the README

Save the file, then run:

```powershell
git status
Send me the output only.

We will then commit this final README and move to the testing evidence, which is one of the important remaining judging requirements.

give me only content i need to write in need to write in readme file please only that thing
# DocuLens AI

## Evidence-First Intelligent Document Investigator

**ALGOTHON'26 — PS ALG-AI-02: Intelligent Document Investigator**

DocuLens AI is an intelligent document investigation platform that allows users to upload multiple documents, ask natural-language questions, retrieve supporting evidence, compare information across sources, detect conflicts, and communicate uncertainty instead of confidently guessing.

The system treats document question answering as an **investigation problem**, not simply a retrieval problem.

---

## Problem Statement

Important information is often distributed across multiple documents such as:

- Employee handbooks
- HR policies
- Contracts
- Reports
- PDFs
- Word documents
- Text files
- Scanned documents
- Images

Traditional document search forces users to manually inspect every file.

A conventional RAG system can also produce a single confident answer even when two documents disagree.

DocuLens AI addresses this by retrieving relevant evidence, comparing claims across documents, verifying supporting citations, detecting conflicts, and communicating uncertainty.

---

## Key Features

### 1. Multi-Document Investigation

Upload multiple documents and investigate information across the complete document collection.

Supported formats:

- PDF
- DOCX
- TXT
- PNG
- JPG / JPEG

### 2. Text Extraction and OCR

DocuLens extracts text from uploaded documents.

For image-based or scanned content, OCR is used to extract readable text before indexing.

The system preserves document and page information so retrieved evidence can be traced back to its source.

### 3. Hybrid Retrieval

DocuLens combines:

- Vector similarity search
- BM25 keyword retrieval

This allows the system to handle both semantic questions and exact information such as:

- Names
- Numbers
- Dates
- Amounts
- Policy values

### 4. Evidence-Grounded Answers

Supported answers can include:

- Source filename
- Page number
- Section
- Direct supporting quote
- Evidence strength
- Investigation trace

Citations are verified against the indexed source text before being presented as verified evidence.

### 5. Conflict Detection

DocuLens compares information across documents and identifies cases where different documents provide different values for the same fact.

Example:

```text
Company Policy
Remote work: 3 days per week

HR Update
Remote work: 2 days per week
Instead of silently selecting one value, DocuLens surfaces the competing claims.

6. Uncertainty Handling
DocuLens does not assume that every question has an answer.

The system uses five investigation verdicts:

Verdict	Meaning
CONFIRMED	Supporting evidence is sufficient and verified
CONFLICT	Multiple sources provide conflicting claims
SUPERSEDED	A newer or authoritative value can be identified
UNCERTAIN	Evidence exists but is not sufficient for a reliable conclusion
NOT_FOUND	The indexed documents do not contain enough information
7. Citation Verification
DocuLens checks whether supporting quotes actually exist in the indexed document text.

This helps reduce unsupported citations and hallucinated references.

8. Investigation Trace
A typical investigation follows:

Question
   ↓
Retrieve Passages
   ↓
Relevance Filtering
   ↓
Compare Claims
   ↓
Conflict Analysis
   ↓
Citation Verification
   ↓
Evidence Strength
   ↓
Final Verdict
How It Works
Upload Documents
       ↓
Text Extraction / OCR
       ↓
Chunking
       ↓
Indexing
       ↓
Hybrid Retrieval
       ↓
Evidence Collection
       ↓
Claim Comparison
       ↓
Conflict Detection
       ↓
Citation Verification
       ↓
Investigation Verdict
Step 1 — Upload
The user uploads one or more supported documents.

Step 2 — Extract
The backend extracts text from the uploaded documents and uses OCR when necessary.

Step 3 — Chunk
Extracted content is divided into smaller passages while preserving document metadata.

Step 4 — Index
Document chunks are indexed using vector search and BM25 retrieval.

Step 5 — Investigate
The user asks a natural-language question.

Step 6 — Retrieve Evidence
Relevant passages are retrieved and filtered according to relevance.

Step 7 — Compare Claims
The system compares relevant claims across documents.

Step 8 — Verify
Supporting citations are checked against the indexed source text.

Step 9 — Generate Verdict
The system returns the answer together with its evidence, verdict, conflict information, and investigation trace.

Evidence Strength
DocuLens uses a heuristic evidence score from:

0 - 100
The system also reports evidence strength such as:

STRONG
MODERATE
WEAK
NONE
The evidence score is a heuristic evidence score, not a probability or confidence percentage.

Architecture
DocuLens AI follows an evidence-first architecture combining document processing, hybrid retrieval, LLM reasoning, citation verification, and conflict detection.

DocuLens AI Architecture

Major Components
Frontend

React
Investigation interface
Document upload
Evidence display
Conflict Center
Backend

FastAPI
Document processing
Retrieval
Investigation
Citation verification
Conflict analysis
Document Processing

PDF extraction
DOCX extraction
TXT processing
OCR for image/scanned documents
Retrieval

Vector similarity search
BM25 keyword retrieval
Hybrid retrieval
Storage

SQLite
Chroma vector store
LLM

Google Gemini API
Technology Stack
Frontend
React
Vite
JavaScript
CSS
Lucide React
Backend
Python
FastAPI
Uvicorn
Document Processing
PyMuPDF
python-docx
RapidOCR
OpenCV
Retrieval
Chroma
BM25
Vector similarity search
Storage
SQLite
LLM
Google Gemini API
Project Structure
DocLens-AI/
│
├── backend/
│   ├── app/
│   ├── sample_documents/
│   └── test_documents/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── architecture.png
│
├── .gitignore
└── README.md
API Endpoints
Method	Endpoint	Purpose
GET	/api/health	Backend health check
GET	/api/documents	List uploaded documents
POST	/api/documents/upload	Upload and process a document
DELETE	/api/documents/{doc_id}	Delete a document
POST	/api/investigate	Investigate a natural-language question
GET	/api/conflicts	Detect and retrieve document conflicts
Local Setup
Prerequisites
Python 3.11
Node.js
npm
Git
Clone Repository
git clone https://github.com/Nitesh71332/DocLens-AI.git
cd DocLens-AI

Backend Setup
cd backend
..\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

Backend:

http://127.0.0.1:8000
Frontend Setup
Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
Environment Variables
Create/configure the backend .env file:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
API keys must never be committed to GitHub.

Example Investigation
Question:

What is Rahul Kumar's annual salary?
Example result:

Answer:
Rahul Kumar's annual salary is ₹8,40,000.

Verdict:
CONFIRMED

Evidence Strength:
MODERATE

Source:
employee_handbook.txt

Page:
1

Section:
Annual Salary
The answer is supported by a directly verified source quote.

Conflict Detection Example
Document 1:

Employee Handbook

Probation Period:
6 months
Document 2:

HR Policy

Probation Period:
3 months
DocuLens identifies the disagreement instead of silently selecting one value.

Expected verdict:

CONFLICT
Testing and Edge Cases
DocuLens has been tested against multiple investigation scenarios.

Test Scenario	Expected Behavior
Known salary question	CONFIRMED
Conflicting probation periods	CONFLICT
Unknown passport number	NOT_FOUND
Known working-hours question	CONFIRMED
Remote-work disagreement	Conflict detected
Multiple uploaded documents	Cross-document retrieval
Image/scanned content	OCR processing
Unsupported question	No unsupported source-backed claim
Evidence Verification
The system verifies that citation quotes exist in the indexed source text before presenting them as verified evidence.

No-Guessing Behavior
For questions where the documents contain no supporting information, DocuLens can return:

NOT_FOUND
instead of inventing an answer.

ALG-AI-02 Requirement Mapping
Requirement	DocuLens Implementation
Multiple document formats	PDF, DOCX, TXT, PNG, JPG/JPEG
Extraction/indexing	Document extraction, chunking and Chroma indexing
OCR	RapidOCR/OpenCV
Natural-language Q&A	FastAPI investigation pipeline + LLM
Source references	Filename, page, section and direct quotes
Conflict detection	Cross-document claim comparison
Uncertainty handling	Five investigation verdicts
Evidence grounding	Citation verification
Investigation workflow	Retrieve → Compare → Verify → Verdict
Reliability Principles
Evidence Before Confidence
DocuLens prioritizes source evidence rather than relying only on generated text.

No Evidence Means No Confident Answer
When supporting information cannot be found, the system can return:

NOT_FOUND
Conflicting Evidence Is Surfaced
Different source claims are not silently merged into one answer.

Citations Are Verified
Supporting quotes are checked against indexed source content.

Uncertainty Is Explicit
The system distinguishes between confirmed, conflicting, superseded, uncertain, and unavailable information.

Limitations
OCR accuracy depends on image quality.
Complex document layouts may not extract perfectly.
LLM availability and API quotas can affect investigation responses.
Evidence scoring is heuristic rather than probabilistic.
Complex temporal and organizational reasoning may require further improvement.
The current system focuses on document-grounded investigation rather than unrestricted web research.
Production deployment requires persistent storage configuration for SQLite and Chroma.
Future Improvements
Support for additional document formats
Better table extraction
Improved OCR
Advanced temporal reasoning
Stronger document authority reasoning
Document version tracking
Persistent cloud vector storage
Cloud database support
Authentication and role-based access
Multi-user workspaces
Improved conflict-resolution explanations
Production monitoring and observability
External APIs and AI Disclosure
External API
Google Gemini API is used for language-model reasoning.

API credentials are provided through environment variables and are not stored in the repository.

AI-Assisted Development
AI-assisted development tools were used during implementation for activities including:

Code generation
Debugging
UI development
Documentation assistance
Architecture and implementation guidance
The final application integration, testing, configuration, and validation were performed as part of the project development process.

Project Status
Completed
Multi-document upload
PDF support
DOCX support
TXT support
Image support
OCR pipeline
Document extraction
Document chunking
Vector indexing
BM25 retrieval
Hybrid retrieval
Natural-language investigation
Evidence citations
Citation verification
Evidence scoring
Conflict detection
Conflict Center
Uncertainty-aware verdicts
Investigation trace
React frontend
FastAPI backend
Architecture documentation
Planned
Production deployment
Larger-scale persistent storage
Advanced document version reasoning
Additional automated testing
Improved OCR and table extraction
Demo Workflow
Upload multiple documents.
Ask a factual question.
Inspect the answer and verified evidence.
Ask a question involving conflicting documents.
Open the Conflict Center.
Ask a question that is not present in the documents.
Demonstrate the NOT_FOUND verdict.
This demonstrates the complete investigation workflow:

Upload
  ↓
Retrieve
  ↓
Compare
  ↓
Verify
  ↓
Detect Conflicts
  ↓
Communicate Uncertainty
Repository
https://github.com/Nitesh71332/DocLens-AI

Author
Nitesh Kumar

B.Tech — Computer Science and Engineering
Indian Institute of Information Technology Kottayam

ALGOTHON'26
PS ALG-AI-02 — Intelligent Document Investigator

AI may help build it. But the evidence still has to support the answer.

see you given some text and some normal how you used to give int hat whay you given please dont waste my time reduced some content and give me only what i neeed to write that it all i  text format so that on one click i can copy total
Yes, Captain. I understand. You want one single copyable block, with only the README content, no explanations outside it, and shorter.

Copy everything below into README.md:

# DocuLens AI

## Evidence-First Intelligent Document Investigator

**ALGOTHON'26 — PS ALG-AI-02: Intelligent Document Investigator**

DocuLens AI is an intelligent document investigation platform that allows users to upload multiple documents, ask natural-language questions, retrieve supporting evidence, compare information across sources, detect conflicts, and communicate uncertainty instead of confidently guessing.

## Problem

Important information is often scattered across PDFs, Word documents, text files, images, HR policies, contracts, and reports.

Traditional document search requires users to manually inspect multiple files. Standard RAG systems may also provide a confident answer even when documents disagree.

DocuLens AI solves this by treating document Q&A as an investigation process:

**Retrieve → Compare → Verify → Decide**

## Key Features

### Multi-Document Support

Supports:

- PDF
- DOCX
- TXT
- PNG
- JPG / JPEG

### Document Extraction and OCR

Extracts text from documents and uses OCR for scanned or image-based content while preserving document and page information.

### Hybrid Retrieval

Combines:

- Vector similarity search
- BM25 keyword retrieval

This improves retrieval for both semantic questions and exact values such as names, numbers, dates, and amounts.

### Evidence-Grounded Answers

Answers can include:

- Source filename
- Page number
- Section
- Direct supporting quote
- Evidence strength
- Investigation trace

### Conflict Detection

DocuLens compares claims across documents.

Example:

```text
Company Policy
Remote work: 3 days per week

HR Update
Remote work: 2 days per week
Instead of silently selecting one value, DocuLens identifies the disagreement.

Uncertainty Handling
DocuLens uses five investigation verdicts:

Verdict	Meaning
CONFIRMED	Evidence is sufficient and verified
CONFLICT	Sources provide conflicting claims
SUPERSEDED	A newer or authoritative value is identified
UNCERTAIN	Evidence is insufficient for a reliable conclusion
NOT_FOUND	Supporting information is not present
Citation Verification
Supporting quotes are verified against the indexed document text before being presented as verified evidence.

How It Works
Upload Documents
       ↓
Text Extraction / OCR
       ↓
Chunking and Indexing
       ↓
Hybrid Retrieval
       ↓
Evidence Collection
       ↓
Claim Comparison
       ↓
Conflict Detection
       ↓
Citation Verification
       ↓
Final Verdict
Evidence Strength
DocuLens uses a heuristic evidence score from 0–100 and reports evidence strength such as:

STRONG
MODERATE
WEAK
NONE
The evidence score is a heuristic indicator, not a probability or confidence percentage.

Architecture


The system consists of:

React frontend
FastAPI backend
Document extraction and OCR
Hybrid retrieval using Chroma and BM25
SQLite metadata storage
Gemini-based language-model reasoning
Citation verification
Conflict detection
Uncertainty-aware verdict generation
Technology Stack
Frontend

React
Vite
JavaScript
CSS
Lucide React
Backend

Python
FastAPI
Uvicorn
Document Processing

PyMuPDF
python-docx
RapidOCR
OpenCV
Retrieval

Chroma
BM25
Vector similarity search
Storage

SQLite
LLM

Google Gemini API
Project Structure
DocLens-AI/
├── backend/
├── frontend/
├── sample_documents/
├── test_documents/
├── docs/
│   └── architecture.png
├── .gitignore
└── README.md
API Endpoints
Method	Endpoint	Purpose
GET	/api/health	Health check
GET	/api/documents	List documents
POST	/api/documents/upload	Upload document
DELETE	/api/documents/{doc_id}	Delete document
POST	/api/investigate	Investigate a question
GET	/api/conflicts	Detect document conflicts
Local Setup
Clone
git clone https://github.com/Nitesh71332/DocLens-AI.git
cd DocLens-AI

Backend
cd backend
..\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

Backend:

http://127.0.0.1:8000
Frontend
Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
Environment
Configure the backend .env file:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
API keys must not be committed to GitHub.

Example Investigation
Question:

What is Rahul Kumar's annual salary?
Example:

Answer:
Rahul Kumar's annual salary is ₹8,40,000.

Verdict:
CONFIRMED

Source:
employee_handbook.txt

Page:
1

Section:
Annual Salary
Conflict Example
Employee Handbook
Probation Period: 6 months

HR Policy
Probation Period: 3 months
DocuLens identifies the disagreement and can return:

CONFLICT
Testing
Test	Expected Result
Known salary question	CONFIRMED
Conflicting probation periods	CONFLICT
Unknown passport number	NOT_FOUND
Known working-hours question	CONFIRMED
Remote-work disagreement	Conflict detected
Multiple documents	Cross-document retrieval
Scanned image	OCR processing
DocuLens is designed not to invent answers when supporting evidence is unavailable.

ALG-AI-02 Requirement Mapping
Requirement	Implementation
Multiple formats	PDF, DOCX, TXT, PNG, JPG
Extraction	PyMuPDF, python-docx
OCR	RapidOCR/OpenCV
Indexing	Chroma + BM25
Natural-language Q&A	FastAPI + LLM
Source references	Filename, page, section, quote
Conflict detection	Cross-document claim comparison
Uncertainty handling	Five investigation verdicts
Reliability
DocuLens follows an evidence-first approach:

Evidence before confidence
No unsupported confident answers
Conflicting claims are surfaced
Citations are verified
Uncertainty is explicitly communicated
Limitations
OCR accuracy depends on image quality.
Complex document layouts may not extract perfectly.
LLM API availability and quotas can affect responses.
Evidence scoring is heuristic.
Advanced temporal and authority reasoning can be improved.
Production deployment requires persistent storage for SQLite and Chroma.
Future Improvements
More document formats
Better table extraction
Improved OCR
Advanced temporal reasoning
Document version tracking
Stronger authority reasoning
Cloud database and vector storage
Authentication and multi-user workspaces
Improved conflict resolution
External APIs and AI Disclosure
Google Gemini API is used for language-model reasoning.

API credentials are stored through environment variables and are not committed to the repository.

AI-assisted development tools were used for code generation, debugging, UI development, documentation, and implementation guidance.

Project Status
Completed
Multi-document upload
Document extraction
OCR
Hybrid retrieval
Natural-language investigation
Evidence citations
Citation verification
Evidence scoring
Conflict detection
Conflict Center
Uncertainty-aware verdicts
Investigation trace
React frontend
FastAPI backend
Architecture documentation
GitHub repository
Planned
Production deployment
Larger-scale persistent storage
Advanced document version reasoning
Additional automated testing
Improved OCR and table extraction
Demo Workflow
Upload multiple documents.
Ask a factual question.
Inspect the verified evidence.
Ask a question involving conflicting documents.
Open the Conflict Center.
Ask a question that is not present in the documents.
Demonstrate the NOT_FOUND verdict.
Repository
https://github.com/Nitesh71332/DocLens-AI

Author
Nitesh Kumar

B.Tech — Computer Science and Engineering
Indian Institute of Information Technology Kottayam

ALGOTHON'26
PS ALG-AI-02 — Intelligent Document Investigator

AI may help build it. But the evidence still has to support the answer.

Instead of silently selecting one value, DocuLens identifies the disagreement.

Uncertainty Handling
DocuLens uses five investigation verdicts:

Verdict	Meaning
CONFIRMED	Evidence is sufficient and verified
CONFLICT	Sources provide conflicting claims
SUPERSEDED	A newer or authoritative value is identified
UNCERTAIN	Evidence is insufficient for a reliable conclusion
NOT_FOUND	Supporting information is not present
Citation Verification
Supporting quotes are verified against the indexed document text before being presented as verified evidence.

How It Works
Evidence Strength
DocuLens uses a heuristic evidence score from 0–100 and reports evidence strength such as:

STRONG
MODERATE
WEAK
NONE
The evidence score is a heuristic indicator, not a probability or confidence percentage.

Architecture
The system consists of:

React frontend
FastAPI backend
Document extraction and OCR
Hybrid retrieval using Chroma and BM25
SQLite metadata storage
Gemini-based language-model reasoning
Citation verification
Conflict detection
Uncertainty-aware verdict generation
Technology Stack
Frontend

React
Vite
JavaScript
CSS
Lucide React
Backend

Python
FastAPI
Uvicorn
Document Processing

PyMuPDF
python-docx
RapidOCR
OpenCV
Retrieval

Chroma
BM25
Vector similarity search
Storage

SQLite
LLM

Google Gemini API
Project Structure
API Endpoints
Local Setup
Clone
Backend
Backend:

Frontend
Open another terminal:

Frontend:

Environment
Configure the backend .env file:

API keys must not be committed to GitHub.

Example Investigation
Question:

Example:

Conflict Example
DocuLens identifies the disagreement and can return:

Testing
DocuLens is designed not to invent answers when supporting evidence is unavailable.

ALG-AI-02 Requirement Mapping
Reliability
DocuLens follows an evidence-first approach:

Evidence before confidence
No unsupported confident answers
Conflicting claims are surfaced
Citations are verified
Uncertainty is explicitly communicated
Limitations
OCR accuracy depends on image quality.
Complex document layouts may not extract perfectly.
LLM API availability and quotas can affect responses.
Evidence scoring is heuristic.
Advanced temporal and authority reasoning can be improved.
Production deployment requires persistent storage for SQLite and Chroma.
Future Improvements
More document formats
Better table extraction
Improved OCR
Advanced temporal reasoning
Document version tracking
Stronger authority reasoning
Cloud database and vector storage
Authentication and multi-user workspaces
Improved conflict resolution
External APIs and AI Disclosure
Google Gemini API is used for language-model reasoning.

API credentials are stored through environment variables and are not committed to the repository.

AI-assisted development tools were used for code generation, debugging, UI development, documentation, and implementation guidance.

Project Status
Completed
Multi-document upload
Document extraction
OCR
Hybrid retrieval
Natural-language investigation
Evidence citations
Citation verification
Evidence scoring
Conflict detection
Conflict Center
Uncertainty-aware verdicts
Investigation trace
React frontend
FastAPI backend
Architecture documentation
GitHub repository
Planned
Production deployment
Larger-scale persistent storage
Advanced document version reasoning
Additional automated testing
Improved OCR and table extraction
Demo Workflow
Upload multiple documents.
Ask a factual question.
Inspect the verified evidence.
Ask a question involving conflicting documents.
Open the Conflict Center.
Ask a question that is not present in the documents.
Demonstrate the NOT_FOUND verdict.
Repository

Author
Nitesh Kumar

B.Tech — Computer Science and Engineering
Indian Institute of Information Technology Kottayam

ALGOTHON'26
PS ALG-AI-02 — Intelligent Document Investigator

AI may help build it. But the evidence still has to support the answer.

format this and give me .txt file total please

…



DocuLens_README_Content.txt
Document
Instead of silently selecting one value, DocuLens identifies the disagreement.

### Uncertainty Handling

DocuLens uses five investigation verdicts:

| Verdict    | Meaning                                            |
| ---------- | -------------------------------------------------- |
| CONFIRMED  | Evidence is sufficient and verified                |
| CONFLICT   | Sources provide conflicting claims                 |
| SUPERSEDED | A newer or authoritative value is identified      |
| UNCERTAIN  | Evidence is insufficient for a reliable conclusion |
| NOT_FOUND  | Supporting information is not present              |

### Citation Verification

Supporting quotes are verified against the indexed document text before being presented as verified evidence.

## How It Works

```text
Upload Documents
       ↓
Text Extraction / OCR
       ↓
Chunking and Indexing
       ↓
Hybrid Retrieval
       ↓
Evidence Collection
       ↓
Claim Comparison
       ↓
Conflict Detection
       ↓
Citation Verification
       ↓
Final Verdict
```

## Evidence Strength

DocuLens uses a heuristic evidence score from **0–100** and reports evidence strength such as:

- STRONG
- MODERATE
- WEAK
- NONE

The evidence score is a heuristic indicator, not a probability or confidence percentage.

## Architecture

The system consists of:

- React frontend
- FastAPI backend
- Document extraction and OCR
- Hybrid retrieval using Chroma and BM25
- SQLite metadata storage
- Gemini-based language-model reasoning
- Citation verification
- Conflict detection
- Uncertainty-aware verdict generation

## Technology Stack

**Frontend**

- React
- Vite
- JavaScript
- CSS
- Lucide React

**Backend**

- Python
- FastAPI
- Uvicorn

**Document Processing**

- PyMuPDF
- python-docx
- RapidOCR
- OpenCV

**Retrieval**

- Chroma
- BM25
- Vector similarity search

**Storage**

- SQLite

**LLM**

- Google Gemini API

## Project Structure

```text
DocLens-AI/
├── backend/
├── frontend/
├── sample_documents/
├── test_documents/
├── docs/
│   └── architecture.png
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint                  | Purpose                   |
| ------ | ------------------------- | ------------------------- |
| GET    | `/api/health`             | Health check              |
| GET    | `/api/documents`          | List documents            |
| POST   | `/api/documents/upload`   | Upload document           |
| DELETE | `/api/documents/{doc_id}` | Delete document           |
| POST   | `/api/investigate`        | Investigate a question    |
| GET    | `/api/conflicts`          | Detect document conflicts |

## Local Setup

### Clone

```bash
git clone https://github.com/Nitesh71332/DocLens-AI.git
cd DocLens-AI
```

### Backend

```powershell
cd backend
..\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://127.0.0.1:8000
```

### Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

### Environment

Configure the backend `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

API keys must not be committed to GitHub.

## Example Investigation

Question:

```text
What is Rahul Kumar's annual salary?
```

Example:

```text
Answer:
Rahul Kumar's annual salary is ₹8,40,000.

Verdict:
CONFIRMED

Source:
employee_handbook.txt

Page:
1

Section:
Annual Salary
```

## Conflict Example

```text
Employee Handbook
Probation Period: 6 months

HR Policy
Probation Period: 3 months
```

DocuLens identifies the disagreement and can return:

```text
CONFLICT
```

## Testing

| Test                          | Expected Result          |
| ----------------------------- | ------------------------ |
| Known salary question         | CONFIRMED                |
| Conflicting probation periods | CONFLICT                 |
| Unknown passport number       | NOT_FOUND                |
| Known working-hours question  | CONFIRMED                |
| Remote-work disagreement      | Conflict detected        |
| Multiple documents            | Cross-document retrieval |
| Scanned image                 | OCR processing           |

DocuLens is designed not to invent answers when supporting evidence is unavailable.

## ALG-AI-02 Requirement Mapping

| Requirement          | Implementation                  |
| -------------------- | ------------------------------- |
| Multiple formats     | PDF, DOCX, TXT, PNG, JPG        |
| Extraction           | PyMuPDF, python-docx             |
| OCR                  | RapidOCR/OpenCV                  |
| Indexing             | Chroma + BM25                   |
| Natural-language Q&A | FastAPI + LLM                   |
| Source references    | Filename, page, section, quote  |
| Conflict detection   | Cross-document claim comparison |
| Uncertainty handling | Five investigation verdicts     |

## Reliability

DocuLens follows an evidence-first approach:

- Evidence before confidence
- No unsupported confident answers
- Conflicting claims are surfaced
- Citations are verified
- Uncertainty is explicitly communicated

## Limitations

- OCR accuracy depends on image quality.
- Complex document layouts may not extract perfectly.
- LLM API availability and quotas can affect responses.
- Evidence scoring is heuristic.
- Advanced temporal and authority reasoning can be improved.
- Production deployment requires persistent storage for SQLite and Chroma.

## Future Improvements

- More document formats
- Better table extraction
- Improved OCR
- Advanced temporal reasoning
- Document version tracking
- Stronger authority reasoning
- Cloud database and vector storage
- Authentication and multi-user workspaces
- Improved conflict resolution

## External APIs and AI Disclosure

Google Gemini API is used for language-model reasoning.

API credentials are stored through environment variables and are not committed to the repository.

AI-assisted development tools were used for code generation, debugging, UI development, documentation, and implementation guidance.

## Project Status

### Completed

- Multi-document upload
- Document extraction
- OCR
- Hybrid retrieval
- Natural-language investigation
- Evidence citations
- Citation verification
- Evidence scoring
- Conflict detection
- Conflict Center
- Uncertainty-aware verdicts
- Investigation trace
- React frontend
- FastAPI backend
- Architecture documentation
- GitHub repository

### Planned

- Production deployment
- Larger-scale persistent storage
- Advanced document version reasoning
- Additional automated testing
- Improved OCR and table extraction

## Demo Workflow

1. Upload multiple documents.
2. Ask a factual question.
3. Inspect the verified evidence.
4. Ask a question involving conflicting documents.
5. Open the Conflict Center.
6. Ask a question that is not present in the documents.
7. Demonstrate the `NOT_FOUND` verdict.

## Repository

https://github.com/Nitesh71332/DocLens-AI



# ALGOTHON'26

**PS ALG-AI-02 — Intelligent Document Investigator**

> AI may help build it. But the evidence still has to support the answer.


