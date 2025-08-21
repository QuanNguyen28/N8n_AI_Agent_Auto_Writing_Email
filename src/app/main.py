# src/app/main.py
import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv

try:
    from pydantic_settings import BaseSettings
except Exception:
    try:
        from pydantic import BaseSettings 
    except Exception:
        BaseSettings = object  

load_dotenv()

class Settings(BaseSettings):
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", 8000))
    debug: bool = os.getenv("APP_DEBUG", "false").lower() in ("1", "true", "yes")

settings = Settings()

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("ai-agent")

app = FastAPI(
    title="AI Agent - FastAPI",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

try:
    from src.app.routers.llm_router import router as llm_router  
    app.include_router(llm_router, prefix="/internal/llm-chat", tags=["llm"])
    logger.info("Registered router: app.routers.llm_router -> /internal/llm-chat")
except Exception as e:
    logger.warning("Could not register app.routers.llm_router: %s", e)

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}

# ---- Startup / Shutdown events (placeholders) ----
@app.on_event("startup")
async def on_startup():
    logger.info("Starting AI Agent service (debug=%s)", settings.debug)

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down AI Agent service")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=settings.debug)
