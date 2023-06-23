from fastapi import FastAPI
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
def handle_init(backend: Backend, settings: Settings) -> None:
    """Initialize the simulation setup"""
    backend.init(settings)


@app.post("/api/ready")
def handle_ready(backend: Backend, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    return backend.ready(settings)


@app.post("/api/start")
def handle_start(backend: Backend, settings: Settings) -> None:
    """Start the simulation"""
    backend.start(settings)


@app.get("/api/status")
def handle_status(backend: Backend) -> dict:
    """Get the running results of the simulation"""
    return backend.status()


@app.post("/api/reset")
def handle_reset(backend: Backend) -> None:
    """Teardown/reset the simulation"""
    backend.reset()
