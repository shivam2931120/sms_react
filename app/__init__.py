from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Disable strict slashes
    app.url_map.strict_slashes = False

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.student import student
    from app.routes.teacher import teacher
    from app.routes.attendance import attendance_bp
    from app.routes.fees import fees_bp
    from app.routes.main import main
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(student)
    app.register_blueprint(teacher)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(fees_bp)
    
    # Import models to ensure they are registered with SQLAlchemy
    from app import models
    
    # Create tables if DATABASE_URL is set (production)
    # Skip if running on Vercel cold start without proper DB
    if os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL'):
        with app.app_context():
            try:
                db.create_all()
                app.logger.info("Database tables created/verified")
            except Exception as e:
                app.logger.error(f"Database setup error: {e}")
                # Don't crash - let the app handle individual route errors
    
    return app
