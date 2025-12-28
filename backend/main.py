from fastapi import FastAPI

from api.birth_routes import router as birth_router

app = FastAPI(title="Jami-Dusu API", version="0.1.0")

app.include_router(birth_router, prefix="/api/v1/birth", tags=["birth"])


@app.get("/health")
def health_check() -> dict:
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}
