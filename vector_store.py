# Implement ChromaDB vector store integration here
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIRECTORY = os.path.join(BASE_DIR, 'dataset')
VECTORSTORE_DIR = os.path.join(BASE_DIR, 'vectorstore')
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

from pydantic import SecretStr
embeddings_model = OpenAIEmbeddings()


collection_name = "pdf_chunks"
vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings_model,
    persist_directory=VECTORSTORE_DIR
)

def add_embeddings(chunks):
    """
    Adds a list of document chunks to the Chroma vector store.
    Each chunk should have a `page_content` attribute containing the text.
    """
    texts = [chunk.page_content for chunk in chunks]
    # for chunk in chunks:
    #     print(f"Chunk metadata: {chunk.metadata}")    
    vector_store.add_texts(texts=texts, metadata=[{"source": chunk.metadata["source"]} for chunk in chunks])
    return len(texts)

def search(question, k=5):
    query_embedding = embeddings_model.embed_query(question)
    """
    Searches the Chroma vector store using a query embedding and returns the top k relevant document texts.
    """
    # LangChain’s Chroma wrapper expects a query string. Since we already have the embedding,
    # we can bypass the embedding step by using the internal search functionality.
    # However, if you want to use the embedding directly, you can use the "similarity_search_by_vector" method.

    results = vector_store.similarity_search_by_vector(query_embedding, k=k)

    # Each result is a Document object from LangChain, so extract the page_content
    retrieved_texts = [doc.page_content for doc in results]
    return retrieved_texts

def clear_vector_store():
    """
    Clears the current data in the Chroma vector store.
    """
    vector_store.delete_collection()
    reset_vector_store()
    print(f"Cleared the vector store collection: {collection_name}")

def reset_vector_store():
    """
    Re-creates and initializes the Chroma vector store collection.
    """
    global vector_store
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings_model,
        persist_directory=VECTORSTORE_DIR
    )
    print(f"Re-created and initialized the vector store collection: {collection_name}")


