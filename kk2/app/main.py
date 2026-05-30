from fastapi import FastAPI, HTTPException, UploadFile, File
import logging
from app.data import load_csv, get_stats
from kk2.app.schemas import (
    AskRequest,
    PromptInput
)
from app.chain.pipeline import oracle_chain


app = FastAPI()

# Configure logging for the application. 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
def health():
    return {"status": "OK"} 

# Endpoint to upload a CSV file. It accepts a file upload, CSV, it raises an HTTP 400 error.
@app.post("/data/upload")
async def upload(file: UploadFile = File(...)):

    logger.info(f"Upload attempt: {file.filename}")

    if not file.filename.endswith(".csv"):
        logger.warning(f"Rejected non-CSV file: {file.filename}")
        raise HTTPException(400, "Only CSV allowed")

    # ✓ FIX: read bytes here, then pass bytes to load_csv
    content = await file.read()

    if not content:
        raise HTTPException(400, "Empty file uploaded")

    try:
        meta = load_csv(content)   # ← pass bytes, not file.file
        logger.info(f"Dataset loaded successfully with {meta['rows']} rows")
        return meta

    except Exception as e:
        logger.error(f"Error occurred while loading CSV: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

#
@app.get("/data/stats")
def stats():

    logger.info("Stats requested")
    stats = get_stats()

    if stats is None:
        logger.warning("Stats requested but no dataset uploaded")
        raise HTTPException(status_code=404, detail="No dataset uploaded")

    return stats


@app.post("/ai/ask")
def ask_ai(body: AskRequest):

    logger.info(f"AI question received: {body.question}")

    stats = get_stats()

    if stats is None:
        logger.warning("AI question asked but no dataset uploaded")
        logger.info(f"AI question failed: {body.question}")

        raise HTTPException(
            status_code=400,
            detail="Dataset must be uploaded before asking questions"
        )
    try:

        chain_input = PromptInput(
            question=body.question,
            stats=stats
        )

        result = oracle_chain.invoke(chain_input)

        logger.info("AI response generated successfully")

        return {
            "question": body.question,
            "answer": result.answer,
            "model": "MockModel"
        }

    except Exception as e:

        logger.error(f"AI pipeline failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="AI processing failed"
        )   