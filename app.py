from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import List

app = FastAPI()

UPLOAD_DIRECTORY = "upload"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@app.post("/upload")
async def upload_image(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append({"filename": file.filename, "path": file_path})
    return {"uploaded_files": uploaded_files}

@app.get("/images")
async def list_images():
    files = [{"filename": f, "url": f"/images/{f}", "tags": ["sample"]} for f in os.listdir(UPLOAD_DIRECTORY)]
    return {"images": files}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.delete("/images/{filename}")
async def delete_image(filename: str):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    os.remove(file_path)
    return {"message": f"Image {filename} deleted successfully"}

@app.get("/")
async def root():
    return {"message": "Hello World"}