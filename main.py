from fastapi import FastAPI, UploadFile, HTTPException
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import time
import io
import shutil


app = FastAPI()
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class Question(BaseModel):
    question: str
    

@app.get("/")
def root():
    return {"message": "Hello RAG"}

@app.post("/uploadfile")
async def upload_file(file: UploadFile):
    allowed_extensions = ["txt", "pdf"]

    file_extension = file.filename.split(".")[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    folder = "sources"
    try:
        os.makedirs(folder, exist_ok=True)
        file_location = os.path.join(folder, file.filename)
        file_content = await file.read()
        with open(file_location, "wb+") as file_object:
            file_like_object = io.BytesIO(file_content)
            shutil.copyfileobj(file_like_object, file_object)

        return {"info": "File saved", "filename": file.filename}  # Fixed return statement
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")
        

@app.post("/ask")
async def ask_question(question: Question):
    time.sleep(2)
    if OPENAI_API_KEY is None:
        raise HTTPException(status_code=500, detail="OpenAI API key not set")
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question.question}
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"response": response.choices[0].message.content}





