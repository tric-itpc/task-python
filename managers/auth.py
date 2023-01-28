from datetime import datetime, timedelta
from typing import Optional

import jwt
from decouple import config
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from db import database
from models.enums import RoleType
from models.user import user


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user["id"],
            "exp": datetime.utcnow() + timedelta(minutes=120),
        }
        return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(
                res.credentials, config("JWT_SECRET"), algorithms=["HS256"]
            )
            user_data = await database.fetch_one(
                user.select().where(user.c.id == payload["sub"])
            )
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")


oauth2_scheme = CustomHTTPBearer()


def is_admin_or_staff(request: Request):
    if request.state.user["role"] not in (RoleType.admin, RoleType.staff):
        raise HTTPException(403, "Forbidden")


def is_admin(request: Request):
    if request.state.user["role"] != RoleType.admin:
        raise HTTPException(403, "Forbidden")
