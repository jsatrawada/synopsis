import os

# class Settings:
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     PDF_UPLOAD_PATH = os.getenv("PDF_UPLOAD_PATH", "./uploads")
#     VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
# settings = Settings()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
PUBLICATIONS_DIR = "publications"