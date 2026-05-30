from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "OK"}

DATASET = None


@app.get("/data/stats")
def stats():
    if DATASET is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset uploaded"
        )

    return {"stats": "placeholder"}