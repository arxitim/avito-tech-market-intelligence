from datetime import datetime
from bson.objectid import ObjectId
from base64 import b64decode, b64encode

import pymongo


class MongoDB(object):
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance') or not cls._instance:
            cls._instance = super().__new__(cls)
            connection = pymongo.MongoClient("mongodb+srv://arxitim:TKEq5BBqwC_85_M@avito-tech-mi-untpv"
                                             + ".mongodb.net/test?retryWrites=true&w=majority")
            cls._instance.db = connection["avito-tech"]
        return cls._instance

    def create_secret(self, secret, code_phrase):
        secrets = self._instance.db.secrets
        # secrets.create_index("dt_create", expireAfterSeconds=5 * 60)

        timestamp = datetime.utcnow()
        encrypted_secret = b64encode(secret.encode("UTF-8"))

        secret = {"secret": encrypted_secret, "code_phrase": code_phrase, "dt_create": timestamp}
        secret_id = secrets.insert_one(secret).inserted_id
        return str(secret_id)

    def get_secret(self, secret_id, code_phrase):
        secret_id = ObjectId(secret_id)
        secrets = self._instance.db.secrets

        secret = secrets.find_one({"_id": secret_id})

        if code_phrase == secret["code_phrase"]:
            secrets.delete_one({"_id": secret_id})
            return b64decode(secret["secret"]).decode("UTF-8")
        else:
            return {"error": "wrong code_phrase!"}
