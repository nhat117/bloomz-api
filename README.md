# BloomZ API

This project is a FastAPI-based application that allows users to upload PDF files, extract text from them using OCR, store the extracted text in a vector database, and interact with a fine-tuned language model. Users can also chat directly with the model.

## Features

- Upload PDF files and associate them with a user ID.
- Extract text from PDF files using OCR.
- Store extracted text in a vector database for efficient retrieval.
- List all PDFs uploaded by a user.
- Interact with the model by asking questions or chatting directly.

## Requirements

- Python 3.7+
- `requirements.txt` contains all the necessary dependencies.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/nhat117/bloomz-api.git
    cd bloomz-api
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Tesseract and Poppler (for OCR)**:
    - On Ubuntu:
      ```bash
      sudo apt-get install tesseract-ocr
      sudo apt-get install poppler-utils
      ```
    - On macOS:
      ```bash
      brew install tesseract
      brew install poppler
      ```

## Usage

1. **Start the FastAPI server**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

2. **Upload a PDF**:
    - Use `curl`:
      ```bash
      curl -X POST "http://127.0.0.1:8000/upload_pdf/" -F "user_id=12345" -F "file=@/path/to/your/file.pdf"
      ```
    - Use Postman:
      - Create a new `POST` request to `http://127.0.0.1:8000/upload_pdf/`
      - In the `Body` tab, select `form-data`.
      - Add a key `user_id` with the value as the user ID.
      - Add a key `file` with the type `File` and choose the file to upload.

3. **List uploaded PDFs**:
    - Use `curl`:
      ```bash
      curl -X GET "http://127.0.0.1:8000/list_pdfs/?user_id=12345"
      ```
    - Use Postman:
      - Create a new `GET` request to `http://127.0.0.1:8000/list_pdfs/?user_id=12345`.

4. **Ask a question**:
    - Use `curl`:
      ```bash
      curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"user_id": "12345", "question": "What is the capital of France?"}'
      ```
    - Use Postman:
      - Create a new `POST` request to `http://127.0.0.1:8000/predict`.
      - In the `Body` tab, select `raw` and set the type to `JSON`.
      - Provide the JSON payload: `{"user_id": "12345", "question": "What is the capital of France?"}`.

5. **Chat with the model**:
    - Use `curl`:
      ```bash
      curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{"message": "Hello, how are you?"}'
      ```
    - Use Postman:
      - Create a new `POST` request to `http://127.0.0.1:8000/chat`.
      - In the `Body` tab, select `raw` and set the type to `JSON`.
      - Provide the JSON payload: `{"message": "Hello, how are you?"}`.

## Project Structure

- `main.py`: FastAPI application with endpoints for uploading PDFs, listing uploaded PDFs, performing predictions, and direct chat functionality.
- `model.py`: Contains model and tokenizer initialization, text extraction, and vector database functions.
- `schemas.py`: Defines Pydantic models for request validation.
- `requirements.txt`: Lists all necessary dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
