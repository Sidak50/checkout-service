import uuid

TAX_RATE = 0.05  # demo tax
SHIPPING_FLAT = 5.0

def calculate_subtotal(items):
    return round(sum(i["price"] * i["quantity"] for i in items), 2)

def calculate_total(items):
    subtotal = calculate_subtotal(items)
    tax = round(subtotal * TAX_RATE, 2)
    shipping = 0 if subtotal >= 50 else SHIPPING_FLAT
    return round(subtotal + tax + shipping, 2)

def create_order(items, currency):
    order_id = str(uuid.uuid4())
    total = calculate_total(items)
    return {
        "order_id": order_id,
        "total": total,
        "currency": currency,
        "status": "authorized"
    }
