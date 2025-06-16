from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQL_ALCHEMY_DB_CONNECTION_URL,BACKEND_SERVER_PORT


db = SQLAlchemy()

def setup_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_ALCHEMY_DB_CONNECTION_URL

    db.init_app(app)

    @app.route('/')
    def home():
        return 'Flask app is set up!'


    return app


app = setup_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=BACKEND_SERVER_PORT)