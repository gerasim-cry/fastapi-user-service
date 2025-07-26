from fastapi import FastAPI
from app.handlers import router
from app.models import Base
from app.db import engine
from fastapi.openapi.utils import get_openapi


app = FastAPI(debug=True)

app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My FastAPI App",
        version="1.0.0",
        description="Backend API for User Management with Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemas"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth":[]}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi