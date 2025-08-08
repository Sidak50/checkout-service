from pydantic import BaseModel, Field, conint, conlist

class CartItem(BaseModel):
    product_id: str
    quantity: conint(gt=0) = 1
    price: float = Field(ge=0)

class CheckoutRequest(BaseModel):
    user_id: str
    items: conlist(CartItem, min_length=1)
    currency: str = "USD"
    payment_method: str = "card"
    idempotency_key: str | None = None

class CheckoutResponse(BaseModel):
    order_id: str
    total: float
    currency: str
    status: str
