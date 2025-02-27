import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from config import OPENAI_API_KEY
from vector_store import vector_store


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def process_pdf(file: str):
    loader = PyPDFLoader(file)
    loaded_documents = loader.load()
    documents = []
    # print(f"Number of loaded_documents: {len(loaded_documents)}")
    for doc in loaded_documents:
        # print(f"Document metadata: {doc.metadata}")
        documents.append(Document(page_content=doc.page_content, metadata={"source": doc.metadata}))
       
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    return chunks



