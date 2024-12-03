from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import jwt
from jwt import PyJWKClient, decode
from api.config.settings import settings
from jwt.exceptions import InvalidTokenError

logger = settings.configure_logging()


class JWTMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)

        if getattr(request.state, "public_route", True):
            response = await self.app(scope, receive, send)
            if response:
                await send(response)
            return

        if "Authorization" not in request.headers:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"},
            )
            await self.send_response(send, response)
            return

        token = request.headers["Authorization"].split("Bearer ")[-1]
        try:
            payload = await self.decode_token(token)
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            response = JSONResponse(
                status_code=401, content={"detail": "Token expired"}
            )
            await self.send_response(send, response)
            return
        except jwt.InvalidTokenError:
            response = JSONResponse(
                status_code=401, content={"detail": "Invalid token"}
            )
            await self.send_response(send, response)
            return

        response = await self.app(scope, receive, send)
        if response:
            await send(response)

    async def send_response(self, send, response: JSONResponse):
        if isinstance(response, JSONResponse):
            headers = response.headers
            body = response.body
            await send(
                {
                    "type": "http.response.start",
                    "status": response.status_code,
                    "headers": [(k.encode(), v.encode()) for k, v in headers.items()],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": body,
                }
            )
        else:
            raise ValueError("Invalid response type")

    async def decode_token(self, token: str):
        decoded_token = decode(token, options={"verify_signature": False})
        jwks_client = PyJWKClient(settings.KEYCLOAK_JWK_URI)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            data = decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=f'{decoded_token["aud"]}',
                options={"verify_exp": True},
            )
            return data
        except InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise HTTPException(status_code=401, detail="Not authenticated")
