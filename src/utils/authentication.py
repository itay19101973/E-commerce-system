from datetime import timedelta
import os

from flask import Flask
from flask_jwt_extended import JWTManager

from flask_jwt_extended import get_jwt

revoked_refresh_tokens = set()  # blacklist for tokens to


def revoke_jwt_token():
    jti = get_jwt()['jti']  # JWT ID, unique identifier of the token
    revoked_refresh_tokens.add(jti)  # Add this refresh token's jti to blocklist


def setup_jwt_authentication(app: Flask) -> None:
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required for secure token signing.")
    app.config["JWT_SECRET_KEY"] = secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_, jwt_payload: dict):
        jti = jwt_payload['jti']
        return jti in revoked_refresh_tokens
