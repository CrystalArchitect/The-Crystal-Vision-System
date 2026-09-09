import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.db.session import Base, SessionLocal, engine
from app.middleware.error_handlers import register_error_handlers
from app.models.container import Container

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.get(Container, "cc-container-01") is None:
            db.add(Container(id="cc-container-01", status="running"))
            db.commit()
            logger.info("seeded default container cc-container-01")
    finally:
        db.close()

    yield


app = FastAPI(title="CrystalCore.OS Admin API", version="0.1.0", lifespan=lifespan)

settings = get_settings()
if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

register_error_handlers(app)
app.include_router(api_router)


@app.get("/healthz", tags=["meta"])
def healthz() -> dict:
    return {"status": "ok"}
