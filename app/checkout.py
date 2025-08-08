from flask import Blueprint, request, jsonify
from .schemas import CheckoutRequest, CheckoutResponse
from .service import create_order

bp = Blueprint("checkout", __name__)

@bp.post("/checkout")
def checkout():
    payload = request.get_json(force=True, silent=False)
    data = CheckoutRequest(**payload)  # validate
    result = create_order([i.model_dump() for i in data.items], data.currency)
    resp = CheckoutResponse(**result)
    return jsonify(resp.model_dump()), 201

@bp.get("/health")
def health():
    return {"status": "ok"}, 200
