from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from model import extract_text_from_pdf, store_in_vector_db, query_vector_db, chat, user_indices
from schemas import Query, ChatMessage
import os

app = FastAPI()

# Dictionary to store uploaded files for each user
user_files = {}

@app.post("/upload_pdf/")
async def upload_pdf(user_id: str = Form(...), file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF files are accepted.")
    
    file_location = f"./temp_files/{user_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    text = extract_text_from_pdf(file_location)
    store_in_vector_db(text, user_id)

    if user_id not in user_files:
        user_files[user_id] = []
    
    user_files[user_id].append(file.filename)
    
    return {"filename": file.filename, "status": "Text extracted and stored in vector database for user", "user_id": user_id}

@app.get("/list_pdfs/")
async def list_pdfs(user_id: str):
    if user_id not in user_files:
        raise HTTPException(status_code=404, detail="User ID not found or no files uploaded.")
    return {"user_id": user_id, "files": user_files[user_id]}

@app.post("/predict")
def predict(query: Query):
    try:
        index_id = query_vector_db(query.question, query.user_id)
        if index_id is not None:
            closest_sentence = sentence_model.encode(index_id)
            answer = chat(closest_sentence)
        else:
            answer = chat(query.question)
        return {"question": query.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(message: ChatMessage):
    try:
        answer = chat(message.message)
        return {"message": message.message, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the BloomZ API!"}
