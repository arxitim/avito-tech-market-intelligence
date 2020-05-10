from fastapi import FastAPI

from mongodb import MongoDB

app = FastAPI()


@app.get("/generate")
async def generating(secret: str, code_phrase: str):
    db = MongoDB()
    return {"secret_id": db.create_secret(secret, code_phrase)}


@app.get("/secrets/{secret_id}")
async def geting(secret_id: str, code_phrase: str):
    db = MongoDB()
    return {"secret": db.get_secret(secret_id, code_phrase)}
