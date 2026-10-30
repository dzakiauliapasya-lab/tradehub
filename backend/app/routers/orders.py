from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models import Cart, CartItem, Order, OrderItem, Product, Store, User
from app.schemas import CheckoutRequest, OrderResponse, OrderStatusUpdate
from app.utils import generate_order_number

router = APIRouter(prefix="/api/v1/orders", tags=["Pesanan"])

SHIPPING_COST = Decimal("15000")  # ongkir flat (disederhanakan untuk tugas)


@router.post("/checkout", response_model=OrderResponse, status_code=201)
def checkout(
    data: CheckoutRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("buyer", "seller")),
):
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        raise HTTPException(status_code=400, detail="Keranjang kosong")

    selected_ids = set(data.cart_item_ids)
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.id.in_(selected_ids))
        .all()
    )
    if len(cart_items) != len(selected_ids):
        raise HTTPException(status_code=400, detail="Ada item yang tidak ada di keranjang Anda")

    # 1) KUNCI baris produk (diurutkan berdasarkan id agar tidak saling tunggu / deadlock)
    product_ids = sorted({item.product_id for item in cart_items})
    products = (
        db.query(Product)
        .filter(Product.id.in_(product_ids))
        .order_by(Product.id)
        .with_for_update()
        .all()
    )
    product_map = {p.id: p for p in products}

    # 2) Buat order (kosong dulu)
    order = Order(
        order_number=generate_order_number(),
        buyer_id=user.id,
        shipping_name=data.shipping_name,
        shipping_phone=data.shipping_phone,
        shipping_address=data.shipping_address,
        payment_method=data.payment_method,
        notes=data.notes,
        subtotal=Decimal("0"),
        shipping_cost=SHIPPING_COST,
        total_amount=Decimal("0"),
        payment_status="unpaid",
        status="pending",
    )
    db.add(order)
    db.flush()

    # 3) Cek stok, kurangi stok, catat item
    subtotal = Decimal("0")
    for item in cart_items:
        product = product_map.get(item.product_id)
        store = db.get(Store, product.store_id) if product else None

        if not product or product.status != "active" or not store or store.status != "active":
            raise HTTPException(status_code=400, detail="Ada produk yang sudah tidak tersedia")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stok '{product.name}' tidak cukup (tersisa {product.stock})",
            )

        product.stock -= item.quantity
        if product.stock == 0:
            product.status = "sold_out"

        line_total = product.price * item.quantity
        subtotal += line_total
        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            store_id=product.store_id,
            product_name=product.name,   # SALINAN nama & harga saat beli
            price=product.price,
            quantity=item.quantity,
            subtotal=line_total,
        ))
        db.delete(item)  # hapus dari keranjang

    order.subtotal = subtotal
    order.total_amount = subtotal + SHIPPING_COST

    # 4) SIMPAN SEMUANYA sekaligus
    db.commit()
    db.refresh(order)
    return order

# ---------- fungsi bantu ----------
SELLER_TRANSITIONS = {
    "pending": {"processing", "cancelled"},
    "processing": {"shipped", "cancelled"},
    "shipped": {"completed"},
}
BUYER_TRANSITIONS = {
    "pending": {"cancelled"},
    "shipped": {"completed"},   # pembeli konfirmasi pesanan diterima
}


def seller_store(db: Session, user: User):
    return db.query(Store).filter(Store.user_id == user.id).first()


def seller_has_item(db: Session, order: Order, user: User) -> bool:
    store = seller_store(db, user)
    if not store:
        return False
    return (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order.id, OrderItem.store_id == store.id)
        .first()
        is not None
    )


def restore_stock(db: Session, order: Order):
    for item in order.items:
        if item.product_id is None:
            continue
        product = (
            db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
        )
        if product:
            product.stock += item.quantity
            if product.status == "sold_out":
                product.status = "active"


# ---------- endpoint ----------
@router.get("", response_model=list[OrderResponse])
def my_orders(db: Session = Depends(get_db),
              user: User = Depends(require_role("buyer", "seller"))):
    return (
        db.query(Order).filter(Order.buyer_id == user.id).order_by(Order.created_at.desc()).all()
    )


@router.get("/seller/incoming", response_model=list[OrderResponse])
def seller_orders(db: Session = Depends(get_db), user: User = Depends(require_role("seller"))):
    store = seller_store(db, user)
    if not store:
        return []
    order_ids = db.query(OrderItem.order_id).filter(OrderItem.store_id == store.id)
    return (
        db.query(Order).filter(Order.id.in_(order_ids)).order_by(Order.created_at.desc()).all()
    )


@router.get("/{order_id}", response_model=OrderResponse)
def order_detail(order_id: int, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    order = db.get(Order, order_id)
    allowed = order and (
        user.role == "admin"
        or order.buyer_id == user.id
        or (user.role == "seller" and seller_has_item(db, order, user))
    )
    if not allowed:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

    is_buyer = order.buyer_id == user.id
    is_seller = user.role == "seller" and seller_has_item(db, order, user)
    if not (is_buyer or is_seller):
        raise HTTPException(status_code=404, detail="Pesanan tidak ditemukan")

    allowed = set()
    if is_seller:
        allowed |= SELLER_TRANSITIONS.get(order.status, set())
    if is_buyer:
        allowed |= BUYER_TRANSITIONS.get(order.status, set())

    if data.status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Status '{order.status}' tidak bisa diubah ke '{data.status}' oleh Anda",
        )

    if data.status == "processing":
        order.payment_status = "paid"          # pembayaran disimulasikan
    if data.status == "cancelled":
        restore_stock(db, order)               # stok dikembalikan
        if order.payment_status == "paid":
            order.payment_status = "refunded"

    order.status = data.status
    db.commit()
    db.refresh(order)
    return order