import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from routers import auth, suppliers, buyers, videos, leads, credits, messages, admin

app = FastAPI(
    title="SourcingElf API",
    version="1.0.0",
    docs_url="/docs" if settings.app_env == "development" else None,
    redoc_url="/redoc" if settings.app_env == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/api/v1/auth",      tags=["auth"])
app.include_router(suppliers.router, prefix="/api/v1/suppliers",  tags=["suppliers"])
app.include_router(buyers.router,    prefix="/api/v1/buyers",     tags=["buyers"])
app.include_router(videos.router,    prefix="/api/v1/videos",     tags=["videos"])
app.include_router(leads.router,     prefix="/api/v1/leads",      tags=["leads"])
app.include_router(credits.router,   prefix="/api/v1/credits",    tags=["credits"])
app.include_router(messages.router,  prefix="/api/v1/messages",   tags=["messages"])
app.include_router(admin.router,     prefix="/api/v1/admin",      tags=["admin"])


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "env": settings.app_env}


# Serve frontend static files — must be mounted last so API routes take priority
_frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
