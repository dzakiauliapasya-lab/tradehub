from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.models import Cart, CartItem, Product, Store, User
from app.schemas import CartItemAdd, CartItemResponse, CartItemUpdate, CartResponse

router = APIRouter(prefix="/api/v1/cart", tags=["Keranjang"])

buyer_roles = require_role("buyer", "seller")  # penjual juga boleh berbelanja


def get_or_create_cart(db: Session, user: User) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.flush()
    return cart


def build_cart_response(db: Session, cart: Cart) -> CartResponse:
    rows = db.query(CartItem).filter(CartItem.cart_id == cart.id).order_by(CartItem.id).all()
    items, total = [], Decimal("0")
    for row in rows:
        product = row.product
        subtotal = product.price * row.quantity
        total += subtotal
        items.append(CartItemResponse(
            id=row.id, product_id=product.id, product_name=product.name,
            price=product.price, quantity=row.quantity, stock=product.stock,
            subtotal=subtotal,
        ))
    return CartResponse(items=items, total=total)


@router.get("", response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), user: User = Depends(buyer_roles)):
    cart = get_or_create_cart(db, user)
    db.commit()
    return build_cart_response(db, cart)


@router.post("/items", response_model=CartResponse, status_code=201)
def add_item(data: CartItemAdd, db: Session = Depends(get_db), user: User = Depends(buyer_roles)):
    product = (
        db.query(Product)
        .join(Store, Product.store_id == Store.id)
        .filter(Product.id == data.product_id, Product.status == "active", Store.status == "active")
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Produk tidak tersedia")

    store = db.get(Store, product.store_id)
    if store.user_id == user.id:
        raise HTTPException(status_code=400, detail="Anda tidak bisa membeli produk toko sendiri")

    cart = get_or_create_cart(db, user)
    item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.product_id == product.id)
        .first()
    )

    new_quantity = (item.quantity if item else 0) + data.quantity
    if new_quantity > product.stock:
        raise HTTPException(status_code=400, detail=f"Stok tidak cukup (tersisa {product.stock})")

    if item:
        item.quantity = new_quantity
    else:
        db.add(CartItem(cart_id=cart.id, product_id=product.id, quantity=data.quantity))

    db.commit()
    return build_cart_response(db, cart)


@router.patch("/items/{item_id}", response_model=CartResponse)
def update_item(item_id: int, data: CartItemUpdate,
                db: Session = Depends(get_db), user: User = Depends(buyer_roles)):
    item = (
        db.query(CartItem)
        .join(Cart, CartItem.cart_id == Cart.id)
        .filter(CartItem.id == item_id, Cart.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item keranjang tidak ditemukan")
    if data.quantity > item.product.stock:
        raise HTTPException(status_code=400, detail=f"Stok tidak cukup (tersisa {item.product.stock})")

    item.quantity = data.quantity
    db.commit()
    return build_cart_response(db, db.get(Cart, item.cart_id))


@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(buyer_roles)):
    item = (
        db.query(CartItem)
        .join(Cart, CartItem.cart_id == Cart.id)
        .filter(CartItem.id == item_id, Cart.user_id == user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item keranjang tidak ditemukan")

    cart = db.get(Cart, item.cart_id)
    db.delete(item)
    db.commit()
    return build_cart_response(db, cart)