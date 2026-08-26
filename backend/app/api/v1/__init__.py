from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/ping")
def ping():
    return {"message": "pong"}


@api_router.get("/health")
def health_check():
    return {"status": "healthy", "service": "dad-of-anton-api"}