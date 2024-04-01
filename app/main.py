import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.api import router as api_router
from app.views.views import router as views_router
from app.websocket.websocket import router as websocket_router

app = FastAPI()

static_directory = os.path.join(os.path.dirname(__file__), "static")


@app.get("/service-worker.js")
async def get_service_worker():
    return FileResponse(os.path.join(static_directory, "service-worker.js"))


app.include_router(api_router)
app.include_router(views_router)
app.include_router(websocket_router)
