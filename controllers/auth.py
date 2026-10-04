from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel
from serializers.user import (
    UserLoginSchema,
    UserRegistrationSchema,
    UserSchema,
    UserTokenSchema,
)

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=UserTokenSchema, status_code=201)
def signup(user: UserRegistrationSchema, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    new_user = UserModel(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role="client",
    )

    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = new_user.generate_token()

    return {
        "token": token,
        "message": "Account created successfully",
    }


@router.post("/signin", response_model=UserTokenSchema)
def signin(user: UserLoginSchema, db: Session = Depends(get_db)):
    db_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = db_user.generate_token()

    return {
        "token": token,
        "message": "Login successful",
    }


@router.get("/me", response_model=UserSchema)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user