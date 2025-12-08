import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.lifespan import lifespan
from app.files.router import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.include_router(files_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
