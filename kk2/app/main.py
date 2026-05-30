from fastapi import FastAPI, UploadFile, File, HTTPException
from app.data import load_csv, get_stats
from app.data import load_csv, get_stats
from app.schema import AskRequest, PromptInput
from app.chain.pipline import oracle_chain
from app.config import MODEL_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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

@app.post("/ai/ask")
def ask_ai(body: AskRequest):

    logger.info("Question: %s", body.question)

    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = get_stats()

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Upload a dataset first via POST /data/upload",
        )

    try:
        chain_input = PromptInput(
            question=body.question,
            stats=result,
        )
        output = oracle_chain.invoke(chain_input)
        logger.info("Answer: %s", output.answer[:60])

        return {
            "question": body.question,
            "answer": output.answer,
            "model": MODEL_NAME,
        }

    except Exception as e:
        logger.error("Pipeline error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"AI failed: {str(e)}")