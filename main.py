from fastapi import FastAPI, UploadFile, HTTPException
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import time


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
    folder = "sources"
    os.makedirs(folder, exist_ok=True)
    file_location = os.path.join(folder, file.filename)

    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    return {"info": "File saved", "filename": file.filename}  # Fixed return statement

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





