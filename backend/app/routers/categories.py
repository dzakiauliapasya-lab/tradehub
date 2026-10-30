from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Category, User
from app.schemas import CategoryCreate, CategoryResponse
from app.utils import unique_slug

router = APIRouter(prefix="/api/v1/categories", tags=["Kategori"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    if data.parent_id and not db.get(Category, data.parent_id):
        raise HTTPException(status_code=404, detail="Kategori induk tidak ditemukan")

    category = Category(
        name=data.name,
        slug=unique_slug(data.name, 120),
        description=data.description,
        parent_id=data.parent_id,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category