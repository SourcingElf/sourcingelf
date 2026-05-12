import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
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


_frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

# Explicit per-page routes — registered BEFORE the StaticFiles mount so URL
# matching is deterministic for every page (no edge cases with encoded spaces).
_FRONTEND_PAGES = [
    "Admin Backend.html",
    "Buyer Portal - Applications.html",
    "Buyer Portal - Connected.html",
    "Buyer Portal - Create Task.html",
    "Buyer Portal - Dashboard.html",
    "Buyer Portal - Featured Suppliers.html",
    "Buyer Portal - Hub.html",
    "Buyer Portal - Landing.html",
    "Buyer Portal - Lead Form.html",
    "Buyer Portal - Profile.html",
    "Buyer Portal - Register Login.html",
    "Buyer Portal - Requests.html",
    "Buyer Portal - Tasks.html",
    "IM Chat.html",
    "SourcingElf Homepage.html",
    "Supplier Dashboard - Connected.html",
    "Supplier Dashboard - Credits.html",
    "Supplier Dashboard - Home.html",
    "Supplier Dashboard - Requests.html",
    "Supplier Dashboard - Video Submit.html",
    "Supplier Dashboard - Video.html",
    "Supplier Landing.html",
]


def _make_page_handler(filename: str):
    full_path = os.path.join(_frontend_dir, filename)

    def handler():
        return FileResponse(full_path, media_type="text/html")

    handler.__name__ = "page_" + filename.replace(" ", "_").replace("-", "_").replace(".html", "")
    return handler


for _page in _FRONTEND_PAGES:
    app.add_api_route(
        f"/{_page}",
        _make_page_handler(_page),
        methods=["GET"],
        include_in_schema=False,
    )


# Dead-link aliases — old inline templates link to short lowercase URLs that
# never matched a real file. Redirect them to the actual page so existing
# buttons keep working while the source HTML gets cleaned up.
_DEAD_LINK_ALIASES = {
    # `.html`-suffixed aliases — bundle templates link to short names like
    # "credits.html" instead of the spaced real filenames. Mapped from a
    # global grep over all 22 backup HTMLs (規則 10):
    #   - Supplier portal pages cross-link via these 5 shortnames
    #   - Buyer portal short links (tasks.html, featured.html, lead-form.html,
    #     applications.html, profile.html, auth.html, dashboard.html for buyer,
    #     etc.) are intentionally NOT added here yet — they belong in the
    #     D8-D13 Buyer sprint when those pages get wired up.
    "credits.html":      "Supplier Dashboard - Credits.html",
    "video.html":        "Supplier Dashboard - Video.html",
    "video-submit.html": "Supplier Dashboard - Video Submit.html",
    "connected.html":    "Supplier Dashboard - Connected.html",
    "requests.html":     "Supplier Dashboard - Requests.html",
    "index.html":        "Supplier Dashboard - Home.html",
    # Extensionless aliases — Supplier Dashboard - Home.html uses clean URLs
    # like /credits, /dashboard, /leads, but the real files have spaced names.
    # 19 of the 19 extensionless dead-link occurrences in Home.html resolve
    # via these 7 redirects (the remaining 2 — /leads/<uuid> and /settings —
    # are skipped because the target pages do not exist yet).
    "connected":     "Supplier Dashboard - Connected.html",
    "credits":       "Supplier Dashboard - Credits.html",
    "dashboard":     "Supplier Dashboard - Home.html",
    "leads":         "Supplier Dashboard - Home.html",
    "requests":      "Supplier Dashboard - Requests.html",
    "videos":        "Supplier Dashboard - Video.html",
    "videos/create": "Supplier Dashboard - Video Submit.html",
    # Settings is K12 (not built). Alias to Home so /settings doesn't 404 if
    # the client.js patch hasn't loaded (browser cache / mid-deploy).
    "settings":      "Supplier Dashboard - Home.html",
}


def _make_alias_handler(target: str):
    def handler():
        return RedirectResponse(url=f"/{target}", status_code=302)

    handler.__name__ = "alias_" + target.replace(" ", "_").replace("-", "_").replace(".html", "")
    return handler


for _alias, _target in _DEAD_LINK_ALIASES.items():
    app.add_api_route(
        f"/{_alias}",
        _make_alias_handler(_target),
        methods=["GET"],
        include_in_schema=False,
    )


# Stripe Checkout return URLs — direct page routes (no redirect) so the
# query string from Stripe (e.g. ?session_id=cs_test_xxx) is preserved.
_EXTRA_PAGES = {
    "/credits/success":   "Supplier Credits Success.html",
    "/credits/cancelled": "Supplier Credits Cancelled.html",
}

for _path, _file in _EXTRA_PAGES.items():
    app.add_api_route(
        _path,
        _make_page_handler(_file),
        methods=["GET"],
        include_in_schema=False,
    )


# Serve remaining frontend assets (CSS, JS, images) — mounted last so API
# routes + explicit page routes always take priority.
if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
