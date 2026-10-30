from decimal import Decimal
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Category, OrderItem, Product, ProductImage, Store, User
from app.schemas import (
    ProductCreate, ProductImageCreate, ProductListResponse,
    ProductResponse, ProductUpdate,
)
from app.utils import unique_slug

router = APIRouter(prefix="/api/v1/products", tags=["Produk"])



# ---------- fungsi bantu ----------
def get_seller_store(db: Session, user: User) -> Store:
    store = db.query(Store).filter(Store.user_id == user.id).first()
    if not store:
        raise HTTPException(status_code=400, detail="Anda belum memiliki toko. Buat toko dulu.")
    if store.status == "suspended":
        raise HTTPException(status_code=403, detail="Toko Anda sedang disuspend")
    return store


def get_owned_product(db: Session, product_id: int, user: User) -> Product:
    product = (
        db.query(Product)
        .join(Store, Product.store_id == Store.id)
        .filter(Product.id == product_id, Store.user_id == user.id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan di toko Anda")
    return product


# ---------- endpoint penjual ----------
@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    store = get_seller_store(db, user)

    if data.category_id and not db.get(Category, data.category_id):
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")

    status_value = data.status
    if data.stock == 0 and status_value == "active":
        status_value = "sold_out"

    product = Product(
        store_id=store.id,
        category_id=data.category_id,
        name=data.name,
        slug=unique_slug(data.name, 220),
        description=data.description,
        price=data.price,
        stock=data.stock,
        condition_type=data.condition_type,
        status=status_value,
    )
    db.add(product)
    db.flush()  # kirim ke DB sementara agar product.id terisi (belum permanen)

    for index, url in enumerate(data.image_urls):
        db.add(ProductImage(product_id=product.id, image_url=url,
                            is_primary=(index == 0), sort_order=index))

    db.commit()
    db.refresh(product)
    return product


@router.get("/mine", response_model=list[ProductResponse])
def my_products(db: Session = Depends(get_db), user: User = Depends(require_role("seller"))):
    store = db.query(Store).filter(Store.user_id == user.id).first()
    if not store:
        return []
    return db.query(Product).filter(Product.store_id == store.id).order_by(Product.id.desc()).all()

@router.get("", response_model=ProductListResponse)
def list_products(
    q: Optional[str] = Query(default=None, description="Kata kunci nama produk"),
    category_id: Optional[int] = None,
    min_price: Optional[Decimal] = Query(default=None, ge=0),
    max_price: Optional[Decimal] = Query(default=None, ge=0),
    sort: Literal["newest", "price_asc", "price_desc", "name"] = "newest",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Product)
        .join(Store, Product.store_id == Store.id)
        .filter(Product.status == "active", Store.status == "active")
    )

    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    order_options = {
        "newest": Product.created_at.desc(),
        "price_asc": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "name": Product.name.asc(),
    }

    total = query.count()
    items = (
        query.order_by(order_options[sort])
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/{product_id}", response_model=ProductResponse)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .join(Store, Product.store_id == Store.id)
        .filter(Product.id == product_id, Product.status.in_(["active", "sold_out"]),
                Store.status == "active")
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    product = get_owned_product(db, product_id, user)

    if product.status == "blocked":
        raise HTTPException(status_code=403, detail="Produk diblokir admin dan tidak bisa diubah")

    changes = data.model_dump(exclude_unset=True)
    if "category_id" in changes and changes["category_id"] and not db.get(Category, changes["category_id"]):
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")

    for field, value in changes.items():
        setattr(product, field, value)

    # sinkronkan status dengan stok
    if product.stock == 0 and product.status == "active":
        product.status = "sold_out"
    elif product.stock > 0 and product.status == "sold_out":
        product.status = "active"

    db.commit()
    db.refresh(product)
    return product


@router.post("/{product_id}/images", response_model=ProductResponse, status_code=201)
def add_product_image(
    product_id: int,
    data: ProductImageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    product = get_owned_product(db, product_id, user)

    if data.is_primary:
        for img in product.images:
            img.is_primary = False

    db.add(ProductImage(product_id=product.id, image_url=data.image_url,
                        is_primary=data.is_primary or len(product.images) == 0,
                        sort_order=len(product.images)))
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("seller")),
):
    product = get_owned_product(db, product_id, user)

    # Kalau produk sudah pernah dibeli, jangan hapus (riwayat order & ulasan harus aman)
    has_orders = db.query(OrderItem).filter(OrderItem.product_id == product.id).first()
    if has_orders:
        product.status = "draft"
        db.commit()
        return {"message": "Produk pernah terjual, jadi hanya disembunyikan (draft)"}

    db.delete(product)
    db.commit()
    return {"message": "Produk berhasil dihapus"}