from app.storage.database import Base,engine
from app.storage.models import Document,Page,Chunk

Base.metadata.create_all(bind=engine)

print("DocuLens database initialized successfully.")