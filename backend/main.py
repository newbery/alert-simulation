from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .dispatch import Backend
from .settings import Settings

app = FastAPI()

app.mount("/app", StaticFiles(directory="frontend/build", html=True), name="home")
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")


@app.get("/")
def redirect(backend: Backend):
    """Redirect to React app page"""
    return RedirectResponse(url="/app/", status_code=302)


@app.post("/api/init")
def handle_init(backend: Backend, settings: Settings) -> dict:
    """Initialize the simulation setup"""
    return backend.init(settings)


@app.post("/api/ready")
def handle_ready(backend: Backend, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    return backend.ready(settings)


@app.post("/api/start")
def handle_start(backend: Backend, settings: Settings) -> dict:
    """Start the simulation"""
    return backend.start(settings)


@app.post("/api/status")
def handle_status(backend: Backend, settings: Settings) -> dict:
    """Get the running results of the simulation"""
    return backend.status(settings)


@app.post("/api/reset")
def handle_reset(backend: Backend, settings: Settings) -> dict:
    """Teardown/reset the simulation"""
    return backend.reset(settings)
