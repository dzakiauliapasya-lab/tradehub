from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Store, User
from app.schemas import StoreCreate, StoreResponse, StoreUpdate
from app.utils import unique_slug

router = APIRouter(prefix="/api/v1/stores", tags=["Toko"])


@router.post("", response_model=StoreResponse, status_code=201)
def create_store(
    data: StoreCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    if db.query(Store).filter(Store.user_id == user.id).first():
        raise HTTPException(status_code=400, detail="Anda sudah memiliki toko")

    store = Store(
        user_id=user.id,
        name=data.name,
        slug=unique_slug(data.name, 180),
        description=data.description,
        address=data.address,
        status="pending",
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


@router.get("/me", response_model=StoreResponse)
def my_store(db: Session = Depends(get_db), user: User = Depends(require_role("seller"))):
    store = db.query(Store).filter(Store.user_id == user.id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Anda belum memiliki toko")
    return store


@router.put("/me", response_model=StoreResponse)
def update_my_store(
    data: StoreUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    store = db.query(Store).filter(Store.user_id == user.id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Anda belum memiliki toko")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(store, field, value)
    db.commit()
    db.refresh(store)
    return store


@router.get("/{store_id}", response_model=StoreResponse)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.get(Store, store_id)
    if not store or store.status != "active":
        raise HTTPException(status_code=404, detail="Toko tidak ditemukan")
    return store