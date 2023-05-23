from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .user_dto import UserDTO, UpdateUserDTO, SearchUsersDTO
from ...utils.db import get_pg_conn
from ...middleware.auth import jwt_middleware
from ...models import User


router = APIRouter()


# Online users
# @router.get("/online/")
# def get_online_users(rd: Redis = Depends(get_redis_conn)):
#     online_users = rd.smembers("users.online")
#     return online_users


@router.post("/")
def create_user(userDTO: UserDTO, db: Session = Depends(get_pg_conn)):
    user = User()
    user.email = userDTO.email
    user.password = userDTO.password
    user.username = userDTO.username

    db.add(user)
    db.commit()
    db.refresh(user)

    return user.to_dict()


@router.put("/{user_id}")
def update_user(
    user_id: str, userDTO: UpdateUserDTO, db: Session = Depends(get_pg_conn)
):
    user: User = db.query(User).filter(User._id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if userDTO.email:
        user.email = userDTO.email

    if userDTO.username:
        user.username = userDTO.username

    db.add(user)
    db.commit()
    db.refresh(user)

    return user.to_dict()


@router.get("/")
def find_all(db: Session = Depends(get_pg_conn), token=Depends(jwt_middleware)):
    print("This is the user token")
    print(token)

    users = db.query(User).all()

    return {"users": users}


@router.get("/{user_id}/")
def find_by_id(user_id: str, db: Session = Depends(get_pg_conn)):
    user: User = db.query(User).filter(User._id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_dict()


@router.delete("/{user_id}/")
def delete(
    user_id: str, db: Session = Depends(get_pg_conn), token=Depends(jwt_middleware)
):
    user: User = db.query(User).filter(User._id == user_id).first()

    print("This is the auth token")
    print(token)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"deleted": True}
