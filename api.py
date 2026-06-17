from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from rag.chain import answer_question
from rag.documents import save_and_load
from rag.store import add_documents


app = FastAPI(title="Developer Onboarding Assistant")


class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Developer Onboarding Assistant API Running"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        docs = await save_and_load(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    chunks = add_documents(docs)
    return {"filename": file.filename, "chunks": chunks, "message": "indexed"}


@app.post("/ask")
def ask(request: Question):
    return answer_question(request.question)
