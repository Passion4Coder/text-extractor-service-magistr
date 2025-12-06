import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan
from app.files.router import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.include_router(files_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
