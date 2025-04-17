import logging
logging.basicConfig(level = logging.DEBUG)

from flask import Flask

from .db_connection import db
from .shopper.shopper_routes import shopper
from .seller.seller_routes import seller
from .analyst.analyst_routes import analyst
from .resources.resources_routes import resources
from .admin.admin_routes import admin
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env.template file
    load_dotenv()

    # Secure config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # these are for the DB object to be able to connect to MySQL
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD')
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')  # Change this to your DB name

    db.init_app(app)

    @app.route("/")
    def home():
        return "<h1>Welcome to reThread </h1>"

    #registering logs
    app.logger.info('current_app(): registering blueprints with Flask app object')
    # Register all blueprints with route prefixes
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(shopper, url_prefix="/shopper")
    app.register_blueprint(seller, url_prefix="/seller")
    app.register_blueprint(analyst, url_prefix="/analyst")
    app.register_blueprint(resources, url_prefix="/resources")

    return app
