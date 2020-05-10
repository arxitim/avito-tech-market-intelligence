from bson.objectid import ObjectId
from base64 import b64decode

import mongodb


def test_is_singlton():
    """
    Checking to make sure that MongoDB is really a Singleton
    """
    a = mongodb.MongoDB()
    b = mongodb.MongoDB()
    assert a is b


def test_write_to_db():
    """
    Checking the DB entry.
    """
    db = mongodb.MongoDB()
    secret_id = ObjectId(db.create_secret("ultra_mega_secret", "strong_password"))

    all_secrets = db._instance.db.secrets
    secret = all_secrets.find_one({"_id": secret_id})

    if "strong_password" == secret["code_phrase"]:
        assert "ultra_mega_secret" == b64decode(secret["secret"]).decode("UTF-8")


def test_write_to_db_cyrillic():
    db = mongodb.MongoDB()
    secret_id = ObjectId(db.create_secret("ультра мега секрет", "сильный пароль"))

    all_secrets = db._instance.db.secrets
    secret = all_secrets.find_one({"_id": secret_id})

    if "сильный пароль" == secret["code_phrase"]:
        assert "ультра мега секрет" == b64decode(secret["secret"]).decode("UTF-8")


def test_write_to_db_mixed():
    db = mongodb.MongoDB()
    secret_id = ObjectId(db.create_secret("ultra_mega_секрет", "strong_password"))

    all_secrets = db._instance.db.secrets
    secret = all_secrets.find_one({"_id": secret_id})

    if "strong_password" == secret["code_phrase"]:
        assert "ultra_mega_секрет" == b64decode(secret["secret"]).decode("UTF-8")


def test_only_once_read():
    """
    Checking to see if reading is really only available once.
    """
    db = mongodb.MongoDB()
    secret_id = db.create_secret("ultra_mega_секрет", "strong_password")

    secret = db.get_secret(secret_id, "strong_password")

    if secret != "ultra_mega_секрет":
        assert False

    assert db._instance.db.secrets.find_one({"_id": ObjectId(secret_id)}) is None
