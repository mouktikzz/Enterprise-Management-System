from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from .extensions import db, login_manager, migrate
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            "sqlite:///" + os.path.join(app.instance_path, "ems.db"),
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    
    from .extensions import db, login_manager, migrate
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)
    @login_manager.user_loader
    def _load_user(user_id):
        from .models import User
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None
    from .blueprints.core import bp as core_bp
    app.register_blueprint(core_bp)
    from .blueprints.dashboard import bp as dash_bp
    app.register_blueprint(dash_bp)
    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from .blueprints.departments import bp as dep_bp
    app.register_blueprint(dep_bp)
    from .blueprints.employees import bp as emp_bp
    app.register_blueprint(emp_bp)
    from .blueprints.projects import bp as proj_bp
    app.register_blueprint(proj_bp)
    from .blueprints.tasks import bp as tasks_bp
    app.register_blueprint(tasks_bp)
    
    
    # Configure file logging
    log_path = os.path.join(app.instance_path, 'error.log')
    os.makedirs(app.instance_path, exist_ok=True)
    handler = RotatingFileHandler(log_path, maxBytes=1024*256, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    return app