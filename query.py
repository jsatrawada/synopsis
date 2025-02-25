from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import openai
from pdf_ingest import process_pdf
from openai import OpenAI
from vector_store import search
from vector_store import add_embeddings, clear_vector_store
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY, PUBLICATIONS_DIR

from vector_store import vector_store

app = FastAPI()
openai.api_key = OPENAI_API_KEY

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/ingest_pdf/")
async def ingest_pdf(file: UploadFile = File(...)):
    os.makedirs(PUBLICATIONS_DIR, exist_ok=True)
    file_location = os.path.join(PUBLICATIONS_DIR, str(file.filename))
    # with open(file_location, "wb") as f:
    #     shutil.copyfileobj(file.file, f)
    chunks = process_pdf(file_location)
    count = add_embeddings(chunks)
    return {"message": f"Processed and added {count} chunks", "filename": file.filename}

@app.post("/generate_evidence/")
async def generate_evidence(question: str = Form(...)):
    
    retrieved_chunks = search(question,5)
    context = "\n".join(retrieved_chunks)
    prompt = (
        f"Using the following context, answer the question:\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.2,
    )

    # Return the answer from the response
    return {"question": question, "answer": completion.choices[0].message}

@app.post("/clear_vector_store/")
async def clear_store():
    clear_vector_store()
    return {"message": "Vector store cleared successfully"}
    