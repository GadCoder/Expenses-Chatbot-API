import hashlib


def hash_chat_id(chat_id: str) -> str:
    return hashlib.sha256(chat_id.encode()).hexdigest()
