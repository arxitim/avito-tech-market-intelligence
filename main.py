import json
import uuid

from fastapi import FastAPI


app = FastAPI()


def create_secret(secret, code_phrase):
    secret_id = uuid.uuid4().hex
    secret_instance = {'secret': secret, 'code_phrase': code_phrase}

    with open("secrets.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}

    with open("secrets.json", "w") as f:
        data[secret_id] = secret_instance
        json.dump(data, f, indent=4)

    return secret_id


def get_secret(secret_id, code_phrase):
    with open("secrets.json", "r") as f:
        secrets = json.load(f)

    secret = secrets.get(secret_id, {'secret': '', 'code_phrase': ''})

    if secret["code_phrase"] == code_phrase:
        return secrets[secret_id]["secret"]
    else:
        return "wrong code phrase or secret_id!"


@app.get("/generate")
async def generating(secret: str, code_phrase: str):
    return {"secret_id": create_secret(secret, code_phrase)}


@app.get("/secrets/{secret_id}")
async def geting(secret_id: str, code_phrase: str):
    return {"secret": get_secret(secret_id, code_phrase)}
