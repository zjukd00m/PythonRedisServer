import pytz
from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .auth_dto import LoginDTO
from .user_dto import UserDTO
from ...models import User
from ...utils.db import get_pg_conn
from ...utils.auth import hash_password, verify_password
from ...utils.jwtokens import encode_jwt_payload, decode_jwt_payload


router = APIRouter()


@router.post("/login")
async def login(loginDTO: LoginDTO, db: Session = Depends(get_pg_conn)):
    user = db.query(User).filter(User.email == loginDTO.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not verify_password(loginDTO.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    payload = {
        "email": user.email,
        "username": user.username,
    }

    token = encode_jwt_payload(payload)

    expires_at = datetime.utcnow() + timedelta(minutes=60)

    json_response = JSONResponse(content={"token": token})

    json_response.set_cookie(
        "auth_cookie",
        token,
        max_age=3600,
        httponly=False,
        path="/",
        secure=False,
        expires=expires_at.astimezone(pytz.UTC).isoformat(),
    )

    return json_response


@router.post("/register")
def register(userDTO: UserDTO, db: Session = Depends(get_pg_conn)):
    # Hash the user password
    hashed_password = hash_password(userDTO.password)

    user = User()
    user.email = userDTO.email
    user.username = userDTO.username
    user.password = hashed_password

    db.add(user)
    db.commit()
    db.refresh(user)

    # Store the user in the database
    return JSONResponse(
        content={
            "_id": str(user._id),
            "email": user.email,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "username": user.username,
        }
    )


@router.post("/logout")
def logout(request: Request):
    """
    Expire the session cookie
    """
    auth_cookie = request.cookies.get("auth_cookie")

    if not auth_cookie:
        raise HTTPException(status_code=404, detail="Missing authentication cookie")

    json_response = JSONResponse(content={"logout": True})

    expires_at = datetime.utcnow()

    json_response.set_cookie(
        "auth_cookie",
        "",
        max_age=0,
        expires=expires_at.astimezone(pytz.UTC).isoformat(),
        path="/",
        secure=False,
        httponly=False,
    )

    return json_response
