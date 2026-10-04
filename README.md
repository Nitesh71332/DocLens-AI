DocuLens AI
Evidence-first document investigator for ALGOTHON'26 --- PS
ALG-AI-02
DocuLens AI lets users upload multiple documents, ask natural-language
questions, retrieve supporting evidence, detect conflicting information,
and avoid unsupported answers.
Features
- Multiple document formats: PDF, DOCX, TXT, PNG, JPG
- Document extraction, chunking, and indexing
- Natural-language investigation
- Verified source quotes with page/section references
- Conflict detection and conflict resolution
- CONFIRMED, CONFLICT, SUPERSEDED, UNCERTAIN, and NOT_FOUND
  verdicts
- Evidence strength and investigation trace
- OCR support for scanned/image documents
Tech Stack
- Frontend: React + Vite
- Backend: FastAPI + Python
- Storage: SQLite + Chroma
- Retrieval: Vector search + BM25 hybrid retrieval
- LLM: Google Gemini
- OCR: RapidOCR + OpenCV
Project Structure
DocLens-AI/
├── backend/
├── frontend/
├── docs/
├── .env
└── README.md
Run Locally
1. Start Backend
Open PowerShell:
cd C:\Users\NITESH\OneDrive\Desktop\vscode\DocLens-AI\backend
..\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
Backend runs at:
http://127.0.0.1:8000
Keep this terminal running.
2. Start Frontend
Open a second PowerShell:
cd C:\Users\NITESH\OneDrive\Desktop\vscode\DocLens-AI\frontend
npm run dev
Open:
http://localhost:5173/
Demo Workflow
1. Upload multiple documents.
2. Ask a question in Investigate.
3. Review the answer and verdict.
4. Check verified source quotes in Evidence.
5. Open Conflict Center to compare conflicting claims.
6. Test an unsupported question and verify that DocuLens returns
   NOT_FOUND instead of inventing an answer.
Example Questions
What is Rahul Kumar's annual salary?
What is the probation period?
How many days of annual leave are employees entitled to?
What is the company's office address?
API
  Method   Endpoint                    Purpose
  GET      /api/health               Backend health
  GET      /api/documents            List documents
  POST     /api/documents/upload     Upload document
  DELETE   /api/documents/{doc_id}   Delete document
  POST     /api/investigate          Investigate a question
  GET      /api/conflicts            Detect document conflicts
Environment
Create/configure the backend .env with the Gemini API key and model
settings.
Never commit .env or API keys to GitHub.
Testing
Verified locally:
- Confirmed factual answers with source citations
- Conflict detection across multiple documents
- Conflict resolution using policy amendments
- NOT_FOUND for unsupported questions
- Evidence panel and investigation trace
- Multiple-document indexing
Limitations
- LLM responses depend on available model/API quota.
- Conflict resolution depends on the evidence and metadata present in
  uploaded documents.
- Current storage is local SQLite + Chroma, so production deployment
  should use persistent storage.
AI / External API Disclosure
DocuLens AI uses Google Gemini for language-model reasoning. OCR and
retrieval components are implemented using the technologies listed
above. AI-assisted development tools were also used during development.
Repository
GitHub: https://github.com/Nitesh71332/DocLens-AI
ALGOTHON'26
Problem Statement: ALG-AI-02 --- Intelligent Document Investigator
Goal: Provide evidence-grounded answers from multiple documents
while explicitly detecting conflicts and handling uncertainty.