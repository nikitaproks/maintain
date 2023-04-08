from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core import tasks


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/api/docs",
        redoc_url=None
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler(
        "startup", tasks.create_start_app_handler(app))
    app.add_event_handler(
        "shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = get_application()


@app.get("/api/health")
def health():
    return {"message": "ok!"}
