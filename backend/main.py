import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.birth_routes import router as birth_router
from core.storage import init_db

load_dotenv()

app = FastAPI(title="Jami-Dusu API", version="0.2.0")


def _get_allowed_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "*").strip()
    if raw == "*":
        return ["*"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(birth_router, prefix="/api/v1/birth", tags=["birth"])


@app.on_event("startup")
def startup() -> None:
    """애플리케이션 시작 시 DB를 초기화한다."""
    init_db()


@app.get("/health")
def health_check() -> dict:
    """헬스 체크 엔드포인트."""
    return {"status": "ok"}
