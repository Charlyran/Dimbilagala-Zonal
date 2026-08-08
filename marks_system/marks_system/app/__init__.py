from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.school import school_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(school_bp, url_prefix='/school')
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()
        from app.models import User
        if User.query.count() == 0:
            from app.seed import seed_data
            seed_data()
    
    return app
