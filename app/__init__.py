from flask import Flask, send_from_directory
from flask_cors import CORS
from .checkout import bp as checkout_bp
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(checkout_bp)

    # Serve the OpenAPI file (located in the project root)
    @app.get("/openapi.yaml")
    def openapi_spec():
        return send_from_directory(
            os.path.dirname(os.path.dirname(__file__)),  # one level above /app
            "openapi.yaml",
            mimetype="text/yaml"
        )

    # Swagger UI at /docs
    SWAGGER_URL = "/docs"
    API_URL = "/openapi.yaml"
    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Checkout Service"}
    )
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)

