from flask import Flask
from flask_cors import CORS
from .routes.invoices import invoices_bp
from .routes.webhook import webhook_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    app.register_blueprint(invoices_bp, url_prefix='/invoices')
    app.register_blueprint(webhook_bp, url_prefix='/webhook')

    return app