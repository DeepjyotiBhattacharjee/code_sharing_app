from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
from .config import Config
import pymysql
import redis

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Limiter with Redis storage
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        storage_uri=f"redis://localhost:6379/0"  # Use the Redis URI directly
    )

    # Initialize Flask-Talisman
    Talisman(app)

    # Apply proxy fix middleware
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Initialize pymysql connection
    app.config['DB_CONNECTION'] = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

    # Register blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
