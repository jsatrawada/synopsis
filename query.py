from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import openai
from pdf_ingest import process_pdf
from openai import OpenAI
from vector_store import search_vector_store
from vector_store import add_embeddings, clear_vector_store
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY, PUBLICATIONS_DIR
from system_prompt_config import DEFAULT_SYSTEM_PROMPT

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
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    chunks = process_pdf(file_location)
    count = add_embeddings(chunks)
    return {"message": f"Processed and added {count} chunks", "filename": file.filename}

@app.post("/generate_evidence/")
async def generate_evidence(question: str = Form(...), system_prompt: str = Form(None)):
    print(f"Question: {question}")
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT
        
    retrieved_chunks = search_vector_store(question,5)
    context = "\n".join(retrieved_chunks)
    prompt = (
        f"Using the following context, answer the question:\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )
    print(f"System Prompt: {system_prompt}")
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=15000,
        temperature=0.2,
    )

    # Return the answer from the response
    return {"question": question, "answer": completion.choices[0].message}

@app.post("/clear_vector_store/")
async def clear_store():
    clear_vector_store()
    try:
        for filename in os.listdir(PUBLICATIONS_DIR):
            file_path = os.path.join(PUBLICATIONS_DIR, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        return {"message": "All files deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting files: {str(e)}")
    return {"message": "Vector store cleared successfully"}
    