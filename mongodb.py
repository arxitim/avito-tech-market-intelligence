from datetime import datetime
from bson.objectid import ObjectId
from base64 import b64decode, b64encode

import pymongo


class MongoDB(object):
    """
    Responsible for connecting to the database,
    writing the secret to it, reading the secret.

    Built on the Singleton concept.
    """
    _instance = None

    server_auth = "mongodb+srv://arxitim:TKEq5BBqwC_85_M@" +\
                  "avito-tech-mi-untpv" +\
                  ".mongodb.net/test?retryWrites=true&w=majority"

    def __new__(cls):
        if not hasattr(cls, '_instance') or not cls._instance:
            cls._instance = super().__new__(cls)
            connection = pymongo.MongoClient(cls.server_auth)
            cls._instance.db = connection["avito-tech"]
        return cls._instance

    def create_secret(self, secret: str, code_phrase: str) -> str:
        """
        A method that writes a secret into a database
        and returns a secret_id of that entry.

        :param secret: secret message
        :type secret: str
        :param code_phrase: for access control
        :type code_phrase: str
        :return: secret_id in database
        :rtype: str
        """
        secrets = self._instance.db.secrets

        # index creation for an empty collection. CAN BE MODIFIED
        # secrets.create_index("dt_create", expireAfterSeconds=10 * 60)

        timestamp = datetime.utcnow()
        encrypted_secret = b64encode(secret.encode("UTF-8"))  # do not store unencrypted data!

        secret = {
            "secret": encrypted_secret,
            "code_phrase": code_phrase,
            "dt_create": timestamp
        }
        secret_id = secrets.insert_one(secret).inserted_id
        return str(secret_id)

    def get_secret(self, secret_id: str, code_phrase: str) -> str:
        """
        The method makes a query to the database,
        checks the record access by code_phrase and,
        if successful, decrypts and returns the secret text.

        In case code_phrase is incorrect,
        it returns the text with an error.

        :param secret_id: secret_id in the database
        :type secret_id: str
        :param code_phrase: for access control
        :type code_phrase: str
        :return: secret message
        :rtype: str
        """
        secret_id = ObjectId(secret_id)
        secrets = self._instance.db.secrets

        secret = secrets.find_one({"_id": secret_id})
        if not secret:
            return "there is no secret with this id!"

        if code_phrase == secret["code_phrase"]:
            secrets.delete_one({"_id": secret_id})  # the record can only be read once
            return b64decode(secret["secret"]).decode("UTF-8")
        else:
            return "wrong code_phrase!"
