from jose import jwt
from typing import Dict
from datetime import datetime, timedelta

JWT_SECRET = "9de47f59b664f927e0222d3d415634a9bb48004f252b630a15f94e1072aa309e"


def encode_jwt_payload(payload: Dict, expires: int = 1):
    issued_at = datetime.utcnow()
    expires_at = issued_at + timedelta(hours=expires)
    payload["exp"] = expires_at
    payload["iat"] = issued_at
    token = jwt.encode(payload, key=JWT_SECRET, algorithm="HS256")
    return token


def decode_jwt_payload(token: str) -> Dict | None:
    try:
        return jwt.decode(token, key=JWT_SECRET, algorithms="HS256")
    except:
        return None
