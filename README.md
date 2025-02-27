
- `app.py`: Entry point for running the FastAPI server.
- `config.py`: Configuration file for environment variables and settings.
- `pdf_ingest.py`: Handles PDF processing and chunking.
- `query.py`: Defines the FastAPI endpoints for PDF ingestion, evidence generation, and clearing the vector store.
- `requirements.txt`: Lists the dependencies required for the project.
- `streamlit_app.py`: Streamlit frontend for interacting with the FastAPI backend.
- `utils.py`: Contains utility functions.
- `vector_store.py`: Manages the ChromaDB vector store for storing and searching document embeddings.

## Setup

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
    - Create a `.env` file in the root directory.
    - Add the  variablesfollowing:
        ```
        OPENAI_API_KEY=<your_openai_api_key>
        VECTOR_STORE_PATH=./vector_store
        ```
5. Command to run the FastAPI application using the Uvicorn ASGI 
    - uvicorn app:app --reload

## Running the Application

1. Start the FastAPI server:
    ```sh
    python [app.py](http://_vscodecontentref_/8)
    ```

2. Start the Streamlit application:
    ```sh
    streamlit run [streamlit_app.py](http://_vscodecontentref_/9)
    ```

## API Endpoints

- **Ingest PDF**: `POST /ingest_pdf/`
    - Upload a PDF file to be processed and ingested into the vector store.
- **Generate Evidence**: `POST /generate_evidence/`
    - Provide a question to retrieve evidence-based answers.
- **Clear Vector Store**: `POST /clear_vector_store/`
    - Clear the vector store and delete all stored files.

## Usage

1. Open the Streamlit application in your browser.
2. Use the sidebar to upload PDF files and manage the vector store.
3. Enter a question in the main interface to generate evidence-based answers.

## License

This project is licensed under the MIT License.