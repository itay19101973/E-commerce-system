import os
from flask import Flask
from flask_jwt_extended import JWTManager
from config import SQL_ALCHEMY_DB_CONNECTION_URL,BACKEND_SERVER_PORT
from routes.users import users_bp
from db import get_db_connection
from utils.authentication import setup_jwt_authentication

def setup_app():
    app = Flask(__name__)

    #for postgress db
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_ALCHEMY_DB_CONNECTION_URL
    db = get_db_connection()
    db.init_app(app)
    with app.app_context():
        db.create_all()

    #for session managing
    setup_jwt_authentication(app)

    #routs
    app.register_blueprint(users_bp)

    return app


app = setup_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=BACKEND_SERVER_PORT,debug=True)