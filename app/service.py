import uuid
import os
import stripe

# --- pricing rules ---
TAX_RATE = 0.05          # 5% tax
SHIPPING_FLAT = 5.0      # $5 shipping under $50

# --- helpers ---
def calculate_subtotal(items: list[dict]) -> float:
    """Sum of price * quantity, rounded to 2 decimals."""
    return round(sum(i["price"] * i["quantity"] for i in items), 2)

def calculate_total(items: list[dict]) -> float:
    """Subtotal + tax + shipping (free shipping for subtotal >= $50)."""
    subtotal = calculate_subtotal(items)
    tax = round(subtotal * TAX_RATE, 2)
    shipping = 0 if subtotal >= 50 else SHIPPING_FLAT
    return round(subtotal + tax + shipping, 2)

# --- payments ---
def pay_with_stripe(total: float, currency: str, payment_method_id: str | None):
    """
    Create & confirm a Stripe PaymentIntent in TEST mode.

    We force card-only so Stripe won't try redirect payment methods
    (which would require a return_url). This keeps Swagger/Postman tests simple.
    """
    sk = os.getenv("STRIPE_SECRET_KEY")
    if not sk:
        return {"status": "error", "error": "STRIPE_SECRET_KEY not set"}

    stripe.api_key = sk
    amount_cents = int(round(total * 100))

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency.lower(),
            payment_method=payment_method_id or "pm_card_visa",  # default Stripe test card
            confirm=True,
            # Keep it card-only (no redirects)
            payment_method_types=["card"],
            # Alternative (don't use both): automatic methods but never redirect
            # automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        )
        return {"status": intent.status, "payment_intent_id": intent.id}
    except stripe.error.CardError as e:
        # Declines and similar card errors
        return {"status": "declined", "error": str(e)}
    except Exception as e:
        # Any other unexpected error
        return {"status": "error", "error": str(e)}

# --- main orchestration ---
def create_order(
    items: list[dict],
    currency: str,
    use_stripe: bool = False,
    payment_method_id: str | None = None,
):
    """
    Build the order, optionally charge via Stripe, and return the result payload.
    """
    order_id = str(uuid.uuid4())
    total = calculate_total(items)

    status = "authorized"    # mock success if not using Stripe
    payment_info = None

    if use_stripe:
        res = pay_with_stripe(total, currency, payment_method_id)
        status = res.get("status", "error")
        payment_info = res

    return {
        "order_id": order_id,
        "total": total,
        "currency": currency,
        "status": status,
        "payment": payment_info,
    }
