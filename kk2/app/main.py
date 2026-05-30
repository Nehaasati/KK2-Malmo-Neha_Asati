from fastapi import FastAPI, UploadFile, File, HTTPException
from app.data import load_csv, get_stats

app = FastAPI()


@app.post("/data/upload")
async def upload(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    metadata = load_csv(content)

    return metadata