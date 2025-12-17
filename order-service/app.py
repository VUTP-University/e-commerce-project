from flask import Flask
from config import Config
from extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from routes import orders_bp
    app.register_blueprint(orders_bp)
    
    with app.app_context():
        from models import Order  # Import models to register them with SQLAlchemy
        db.create_all()  # Create database tables

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5002, debug=True)