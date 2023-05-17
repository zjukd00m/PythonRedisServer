from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes.auth import auth
from .routes.pub_sub import pub_sub
from .routes.user import user
from .utils.db import init_db


def get_app():
    app = FastAPI()

    app.mount("/static", StaticFiles(directory=Path(".") / "public" / "static"))

    templating = Jinja2Templates(directory=Path(".") / "public" / "html")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def index(request: Request):
        context = {
            "request": request,
        }
        return templating.TemplateResponse("index.html", context=context)

    @app.get("/dashboard")
    def dashboard(request: Request):
        context = {"request": request}
        return templating.TemplateResponse("dashboard.html", context=context)

    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(pub_sub.router, prefix="/api/pub_sub", tags=["PubSub"])
    app.include_router(user.router, prefix="/api/users", tags=["Users"])

    @app.on_event("startup")
    def on_startup():
        print("Server is running")
        init_db()

    return app
