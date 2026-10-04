from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.storage.database import Base, engine
import app.storage.models  # noqa: F401  (registers the tables)
from app.api.documents import router as documents_router
from app.api.investigate import router as investigate_router
from app.api.conflicts import router as conflicts_router

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:                                   # keep the vector index in sync with the database
        from app.retrieval.indexer import ensure_indexed
        ensure_indexed()
    except Exception as e:
        print(f"[startup] index sync skipped: {e}")
    yield


app = FastAPI(title="DocuLens AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(investigate_router)
app.include_router(conflicts_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "DocuLens AI"}