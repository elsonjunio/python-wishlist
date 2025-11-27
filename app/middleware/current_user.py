from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
import jwt

# from datetime import datetime
from core.config import settings

SECRET = settings.JWT_SECRET


class CurrentUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = None

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split()[1]

        if token:
            try:
                payload = jwt.decode(token, SECRET, algorithms=['HS256'])
                request.state.current_user = {
                    'id': payload['sub'],
                    'email': payload['email'],
                    'role': payload.get('role', 'customer'),
                }
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail='Token expired')
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail='Invalid token')
        else:
            request.state.current_user = None

        response = await call_next(request)
        return response
