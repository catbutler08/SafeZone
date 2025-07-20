from fastapi import FastAPI
from .routers import auth, account
from .core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)
app.include_router(account.router)
