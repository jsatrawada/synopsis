FastAPI application using the Uvicorn ASGI
This application UI is https://github.com/jsatrawada/synopsis-gen-ui
- `app.py`: Entry point for running the FastAPI server.
- `config.py`: Configuration file for environment variables and settings.
- `pdf_ingest.py`: Handles PDF processing and chunking.
- `query.py`: Defines the FastAPI endpoints for PDF ingestion, evidence generation, and clearing the vector store.
- `requirements.txt`: Lists the dependencies required for the project.
- `utils.py`: Contains utility functions.
- `vector_store.py`: Manages the ChromaDB vector store for storing and searching document embeddings.

## Setup in local

1. Clone the repository:
    ```sh
    git clone https://github.com/jsatrawada/synopsis.git
    cd synopsis
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    # Add enviorment variable for open_api_key
    export OPENAI_API_KEY= <Oen API key>

5. Command to run the FastAPI application using the Uvicorn ASGI 
    In Local
    - uvicorn app:app --reload



## API Endpoints

- **Ingest PDF**: `POST /ingest_pdf/`
    - Upload a PDF file to be processed and ingested into the vector store.
- **Generate Evidence**: `POST /generate_evidence/`
    - Provide a question to retrieve evidence-based answers.
- **Clear Vector Store**: `POST /clear_vector_store/`
    - Clear the vector store and delete all stored files.

## Usage in local
Need to set up and run the streamlit app 
Look at the ReadMe in https://github.com/jsatrawada/synopsis-gen-ui
streamlit run streamlit_app.py  

## License

This project is licensed under the MIT License.