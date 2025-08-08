from flask import Flask
from flask_cors import CORS
from .checkout import bp as checkout_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(checkout_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
