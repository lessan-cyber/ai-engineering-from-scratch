from contextlib import asynccontextmanager
from fastapi import FastAPI
from qdrant_client import QdrantClient


client: QdrantClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = QdrantClient(url="http://localhost:6333")
    yield
    client = None


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/check_qdrant")
def check_qdrant():
    return {"status": "ok" if client.info() else "error"}
