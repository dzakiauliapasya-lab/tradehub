from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Order, Product, Store, User
from app.schemas import (
    AdminStats, ProductModeration, ProductResponse, StoreResponse,
    StoreStatusUpdate, UserActiveUpdate, UserResponse,
)

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role("admin"))],   # SEMUA endpoint di sini khusus admin
)


@router.get("/stats", response_model=AdminStats)
def platform_stats(db: Session = Depends(get_db)):
    status_rows = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    revenue = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(Order.status == "completed")
        .scalar()
    )
    return AdminStats(
        total_users=db.query(User).count(),
        total_sellers=db.query(User).filter(User.role == "seller").count(),
        total_stores=db.query(Store).count(),
        pending_stores=db.query(Store).filter(Store.status == "pending").count(),
        total_products=db.query(Product).count(),
        total_orders=db.query(Order).count(),
        orders_by_status={status: count for status, count in status_rows},
        total_revenue=revenue,
    )


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()


@router.patch("/users/{user_id}/active", response_model=UserResponse)
def set_user_active(user_id: int, data: UserActiveUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Akun admin tidak bisa dinonaktifkan")
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return user


@router.get("/stores", response_model=list[StoreResponse])
def list_stores(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Store)
    if status:
        query = query.filter(Store.status == status)
    return query.order_by(Store.id).all()


@router.patch("/stores/{store_id}/status", response_model=StoreResponse)
def set_store_status(store_id: int, data: StoreStatusUpdate, db: Session = Depends(get_db)):
    store = db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Toko tidak ditemukan")
    store.status = data.status          # active = verifikasi, suspended = blokir
    db.commit()
    db.refresh(store)
    return store


@router.get("/products", response_model=list[ProductResponse])
def list_all_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id.desc()).all()


@router.patch("/products/{product_id}/moderate", response_model=ProductResponse)
def moderate_product(product_id: int, data: ProductModeration, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    product.status = data.status        # blocked = melanggar aturan
    db.commit()
    db.refresh(product)
    return product