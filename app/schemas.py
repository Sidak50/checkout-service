from pydantic import BaseModel, Field, conint, conlist
from typing import Optional

class CartItem(BaseModel):
    product_id: str
    quantity: conint(gt=0) = 1
    price: float = Field(ge=0)

class CheckoutRequest(BaseModel):
    user_id: str
    items: conlist(CartItem, min_length=1)
    currency: str = "USD"
    payment_method: str = "card"
    idempotency_key: Optional[str] = None
    # Stripe options
    use_stripe: bool = False
    stripe_payment_method_id: Optional[str] = None  # e.g. "pm_card_visa"

class CheckoutResponse(BaseModel):
    order_id: str
    total: float
    currency: str = "USD"
    status: str
    payment: Optional[dict] = None
