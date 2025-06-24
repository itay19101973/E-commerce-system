
from flask import Flask
from config import SQL_ALCHEMY_DB_CONNECTION_URL, BACKEND_SERVER_PORT , PRODUCT_CSV_PATH
from routes.users import users_bp
from routes.products import product_bp
from routes.categories import categories_bp
from database import get_db_connection
from utils.authentication import setup_jwt_authentication
from service.csv_parser_service import load_products_from_csv


def setup_app():
    app = Flask(__name__)

    # for postgres db
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_ALCHEMY_DB_CONNECTION_URL
    db = get_db_connection()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        load_products_from_csv(PRODUCT_CSV_PATH)

    # for session managing
    setup_jwt_authentication(app)

    # load products from csv file


    # routs
    app.register_blueprint(users_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(categories_bp)

    return app


application = setup_app()

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=BACKEND_SERVER_PORT, debug=True)
