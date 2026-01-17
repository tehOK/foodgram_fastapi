from datetime import datetime, timedelta

import bcrypt
import jwt

from config import settings



def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_jwt_path.read_text(),
    algorithm: str = settings.auth.jwt_algorithm,
    expire_minutes: int = settings.auth.access_token_lifetime,
):
    to_encode = payload.copy()
    now = datetime.now()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        #iat=now,
        exp=expire,
    )
    encode = jwt.encode(
        to_encode,
        private_key,
        algorithm,
    )
    return encode


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth.public_jwt_path.read_text(),
    algorithm: str = settings.auth.jwt_algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithm,
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password,
    )
