from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Order, OrderItem, Review, User
from app.schemas import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/api/v1/reviews", tags=["Ulasan"])


@router.post("", response_model=ReviewResponse, status_code=201)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer", "seller")),
):
    item = db.get(OrderItem, data.order_item_id)
    order = db.get(Order, item.order_id) if item else None

    if not item or order.buyer_id != user.id:
        raise HTTPException(status_code=404, detail="Item pesanan tidak ditemukan")
    if order.status != "completed":
        raise HTTPException(status_code=400, detail="Ulasan hanya bisa diberikan setelah pesanan selesai")
    if item.product_id is None:
        raise HTTPException(status_code=400, detail="Produk sudah tidak tersedia")
    if db.query(Review).filter(Review.order_item_id == item.id).first():
        raise HTTPException(status_code=400, detail="Item ini sudah pernah diulas")

    review = Review(
        user_id=user.id,
        product_id=item.product_id,
        order_item_id=item.id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/product/{product_id}", response_model=list[ReviewResponse])
def product_reviews(product_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )