from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- AUTH & USER ----------
class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    role: Literal["buyer", "seller"] = "buyer"
    phone: Optional[str] = Field(default=None, max_length=20)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str
    is_active: bool


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = None

class StoreCreate(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    description: Optional[str] = None
    address: Optional[str] = None


class StoreUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = Field(default=None, max_length=500)


class StoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    slug: str
    description: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    status: str

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: Optional[int] = None
    name: str
    slug: str
    description: Optional[str] = None


# ---------- PRODUCT ----------
class ProductImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    is_primary: bool
    sort_order: int


class ProductImageCreate(BaseModel):
    image_url: str = Field(max_length=500)
    is_primary: bool = False


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    stock: int = Field(ge=0)
    category_id: Optional[int] = None
    condition_type: Literal["new", "used"] = "new"
    status: Literal["draft", "active"] = "active"
    image_urls: list[str] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(default=None, gt=0, max_digits=15, decimal_places=2)
    stock: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None
    condition_type: Optional[Literal["new", "used"]] = None
    status: Optional[Literal["draft", "active"]] = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_id: int
    category_id: Optional[int] = None
    name: str
    slug: str
    description: Optional[str] = None
    price: Decimal
    stock: int
    condition_type: str
    status: str
    created_at: datetime
    images: list[ProductImageResponse] = []


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int

class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: Decimal
    quantity: int
    stock: int
    subtotal: Decimal


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: Decimal

class CheckoutRequest(BaseModel):
    cart_item_ids: list[int] = Field(min_length=1, description="ID item keranjang yang dipilih")
    shipping_name: str = Field(min_length=2, max_length=100)
    shipping_phone: str = Field(min_length=6, max_length=20)
    shipping_address: str = Field(min_length=10)
    payment_method: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: Optional[int] = None
    store_id: Optional[int] = None
    product_name: str
    price: Decimal
    quantity: int
    subtotal: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    buyer_id: int
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    subtotal: Decimal
    shipping_cost: Decimal
    total_amount: Decimal
    payment_method: Optional[str] = None
    payment_status: str
    status: str
    notes: Optional[str] = None
    created_at: datetime
    items: list[OrderItemResponse] = []


class OrderStatusUpdate(BaseModel):
    status: Literal["processing", "shipped", "completed", "cancelled"]

class ReviewCreate(BaseModel):
    order_item_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

# ---------- ADMIN ----------
class UserActiveUpdate(BaseModel):
    is_active: bool


class StoreStatusUpdate(BaseModel):
    status: Literal["pending", "active", "suspended"]


class ProductModeration(BaseModel):
    status: Literal["active", "blocked"]


class AdminStats(BaseModel):
    total_users: int
    total_sellers: int
    total_stores: int
    pending_stores: int
    total_products: int
    total_orders: int
    orders_by_status: dict[str, int]
    total_revenue: Decimal