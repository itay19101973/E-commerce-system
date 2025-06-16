import logging.config
import os

BACKEND_SERVER_PORT = os.getenv("BACKEND_SERVER_PORT", 8000)

POSTGRES_DB = os.getenv("POSTGRES_DB", "e_commerce_site")
POSTGRES_USER = os.getenv("POSTGRES_USER", "e_commerce_manager")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", 123)


# General
APP_NAME = "E-commerce app"


SQL_ALCHEMY_DB_CONNECTION_URL = f"postgresql://{POSTGRES_DB}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"