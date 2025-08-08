from flask import Blueprint, request, jsonify
from .schemas import CheckoutRequest
from .service import create_order

bp = Blueprint("checkout", __name__)

@bp.get("/health")
def health():
    return {"status": "ok"}, 200

@bp.post("/checkout")
def checkout():
    # Parse and validate input
    payload = request.get_json(force=True, silent=False)
    data = CheckoutRequest(**payload)

    # Call service: now supports Stripe when use_stripe=True
    result = create_order(
        [i.model_dump() for i in data.items],
        data.currency,
        use_stripe=data.use_stripe,
        payment_method_id=data.stripe_payment_method_id,
    )

    # Return the dict directly (includes optional "payment" details)
    return jsonify(result), 201

