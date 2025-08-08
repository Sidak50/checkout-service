from app.service import calculate_subtotal, calculate_total, create_order

ITEMS = [
    {"product_id": "p1", "quantity": 2, "price": 10.0},
    {"product_id": "p2", "quantity": 1, "price": 15.0},
]

def test_subtotal():
    assert calculate_subtotal(ITEMS) == 35.0

def test_total_under_50_adds_shipping():
    assert calculate_total(ITEMS) == 41.75  # 35 + 1.75 tax + 5 ship

def test_create_order():
    result = create_order(ITEMS, "USD")
    assert result["currency"] == "USD"
    assert result["status"] == "authorized"
    assert result["total"] == 41.75
    assert "order_id" in result and len(result["order_id"]) > 10
