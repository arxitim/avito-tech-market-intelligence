from fastapi import FastAPI

from mongodb import MongoDB

app = FastAPI()


@app.get("/generate")
async def generating(secret: str, code_phrase: str) -> dict:
    """
    Processes request and makes a query
    to the database for a record.

    :param secret: secret message
    :type secret: str
    :param code_phrase: for access control
    :type code_phrase: str
    :return: response with secret_id
    :rtype: dict
    """
    db = MongoDB()
    return {"secret_id": db.create_secret(secret, code_phrase)}


@app.get("/secrets/{secret_id}")
async def geting(secret_id: str, code_phrase: str) -> dict:
    """
    Processes the request and makes a query
    to the database for reading.

    :param secret_id:
    :type secret_id: str
    :param code_phrase:
    :type code_phrase: str
    :return: decrypted secret or an error
    :rtype: dict
    """
    db = MongoDB()
    return {"secret": db.get_secret(secret_id, code_phrase)}
