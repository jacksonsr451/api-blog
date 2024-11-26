from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import jwt
from api.config.settings import settings

class JWTMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        
        if self.is_protected_route(request):
            if "Authorization" not in request.headers:
                response = JSONResponse(status_code=401, content={"detail": "Authorization header missing"})
                await self.send_response(send, response)
                return

            token = request.headers["Authorization"].split("Bearer ")[-1]
            
            try:
                payload = await self.decode_token(token)
                request.state.user = payload
            except jwt.ExpiredSignatureError:
                response = JSONResponse(status_code=401, content={"detail": "Token expired"})
                await self.send_response(send, response)
                return
            except jwt.InvalidTokenError:
                response = JSONResponse(status_code=401, content={"detail": "Invalid token"})
                await self.send_response(send, response)
                return
            except HTTPException as e:
                response = JSONResponse(status_code=e.status_code, content={"detail": e.detail})
                await self.send_response(send, response)
                return

        response = await self.app(scope, receive, send)
        if response:  # Ensure response is not None before sending
            await send(response)

    def is_protected_route(self, request: Request):
        if any(request.url.path.startswith(route) for route in settings.UNPROTECTED_ROUTES):
            return False
        return True

    async def send_response(self, send, response: JSONResponse):
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": [
                (b"content-type", b"application/json"),
            ],
        })
        await send({
            "type": "http.response.body",
            "body": response.body,
        })

    async def get_jwk(self):
        jwk_uri = settings.KEYCLOAK_JWK_URI
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(jwk_uri)
                response.raise_for_status()
                jwk_data = response.json()
                return jwk_data['keys'][0]
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=500, detail=f"Error fetching JWK from Keycloak: {e}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Request error: {e}")

    def get_public_key(self, jwk):
        return jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

    async def decode_token(self, token: str):
        jwk = await self.get_jwk()
        public_key = self.get_public_key(jwk)
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
