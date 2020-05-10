from datetime import datetime
from bson.objectid import ObjectId

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
        secret = {"secret": secret, "code_phrase": code_phrase, "dt_create": timestamp}
        secret_id = secrets.insert_one(secret).inserted_id
        return str(secret_id)

    def get_secret(self, secret_id, code_phrase):
        secret_id = ObjectId(secret_id)
        secrets = self._instance.db.secrets

        secret = secrets.find_one({"_id": secret_id})

        if code_phrase == secret["code_phrase"]:
            return secret["secret"]
        else:
            return {"error": "wrong code_phrase!"}
