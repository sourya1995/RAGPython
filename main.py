from fastapi import FastAPI, UploadFile
import os

app = FastAPI()

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



