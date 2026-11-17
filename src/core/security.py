from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from dotenv import load_dotenv

import bcrypt
import jwt
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=422,
            detail="La contraseña no puede superar los 72 bytes",
        )

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")

    if len(password_bytes) > 72:
        return False

    return bcrypt.checkpw(
        password_bytes,
        hashed_password.encode("utf-8"),
    )


class JWTManager:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expire_minutes: int = 30,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm,
        )

        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ha expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )


if not SECRET_KEY:
    raise RuntimeError("No se encontró la variable SECRET_KEY")

jwt_manager = JWTManager(secret_key=SECRET_KEY)
