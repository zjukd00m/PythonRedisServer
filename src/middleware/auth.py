from fastapi import Request, HTTPException, status
from starlette.requests import Request
from ..utils.jwtokens import decode_jwt_token


def jwt_middleware(request: Request):
    token = request.cookies.get("auth_cookie")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )

    payload = decode_jwt_token(token)

    request.state.user = payload

    return payload
