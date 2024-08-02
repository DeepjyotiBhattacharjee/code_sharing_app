from flask import Flask
import pymysql.cursors
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

def create_app(config_class='config.ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize security extensions
    csrf = CSRFProtect(app)
    csp = {
        'default-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',  # Allow Bootstrap
            'cdnjs.cloudflare.com'  # Allow CDN for scripts
        ]
    }
    Talisman(app, content_security_policy=csp, force_https=True)

    # Initialize database connection
    def get_db_connection():
        return pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )

    # Register blueprints, routes, etc.
    with app.app_context():
        from . import views
        app.register_blueprint(views.main_bp)

    return app
