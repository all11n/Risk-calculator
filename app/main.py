from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.core.database import engine
from app.models.models import Base
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API для расчета риска сердечно-сосудистых заболеваний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["predictions"])

@app.get("/")
async def root():
    return {
        "message": "CVD Risk Calculator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health_check": "/api/v1/health"
    }

@app.on_event("startup")
async def startup_event():
    print("Server starting...")
    print(f"Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

@app.on_event("shutdown")
async def shutdown_event():
    print("Server shutting down...")
