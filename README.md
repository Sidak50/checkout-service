# Checkout Service

Simple Flask-based Checkout microservice with unit tests and Docker support.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m app
```

Test:
```bash
curl http://localhost:8003/health
curl -X POST http://localhost:8003/checkout           -H "Content-Type: application/json"           -d '{"user_id":"u1","items":[{"product_id":"p1","quantity":2,"price":10.0},{"product_id":"p2","quantity":1,"price":15.0}]}'
```

## Docker
```bash
docker compose up --build
```
fix 
