from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import setup_rag, ask_question
from agent_router import classify_question

app = FastAPI(title="CSE Department AI Chatbot")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "CSE Department AI Chatbot Backend Running"}

@app.post("/ask")
def ask_bot(request: QueryRequest):
    question = request.question
    category = classify_question(question)

    print(f"Question: {question}")
    print(f"Detected Category: {category}")

    index, chunks, metadata = setup_rag(category)
    answer, sources = ask_question(question, index, chunks, metadata, category)

    return {
        "question": question,
        "category": category,
        "answer": answer,
        "sources": list(set(sources))
    }