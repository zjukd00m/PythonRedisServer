from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .user_dto import UserDTO, UpdateUserDTO, SearchUsersDTO
from ...utils.db import get_pg_conn
from ...models import User


router = APIRouter()


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


# @router.get("/")
# def find_all(db: Session = Depends(get_pg_conn)):
#     pass


@router.get("/{user_id}")
def find_by_id(user_id: str, db: Session = Depends(get_pg_conn)):
    user: User = db.query(User).filter(User._id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_dict()


@router.delete("/{user_id}")
def delete(user_id: str, db: Session = Depends(get_pg_conn)):
    user: User = db.query(User).filter(User._id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"deleted": True}
