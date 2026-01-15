import bcrypt
import jwt

from config import settings


def encode_jwt():
    pass
    #encode = jwt.encode()


def decode_jwt():
    pass

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password,
    )
