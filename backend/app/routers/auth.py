from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user

from app.database import get_db
from app.models import User
from app.schemas import (
    LoginRequest, RegisterRequest, TokenResponse, UserResponse, UserUpdate,
)
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    email = data.email.lower()

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    user = User(
        name=data.name,
        email=email,
        password_hash=hash_password(data.password),
        phone=data.phone,
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Akun Anda dinonaktifkan")

    token = create_access_token(user.id, user.role)
    return TokenResponse(access_token=token)
@router.get("/me", response_model=UserResponse)
def get_profile(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UserResponse)
def update_profile(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    # JWT bersifat stateless: server tidak menyimpan token.
    # Logout dilakukan frontend dengan MENGHAPUS token dari penyimpanan browser.
    return {"message": "Logout berhasil. Hapus token di sisi client."}