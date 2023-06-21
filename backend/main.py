
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from . import dispatch
from .settings import Config, Settings

app = FastAPI()

app.mount("/app", StaticFiles(directory="frontend/build", html=True), name="home")
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

#templates = Jinja2Templates(directory="frontend/build")


# The following CORS middleware setup is a placeholder
# in case we find we need it later. Sometimes we need to do
# this when we have cross-origin requests originating from
# different protocols, IPs, domain names, or ports.
#
# For the current development case, we're launching the frontend
# in "development mode" and using "http-proxy-middleware" on the
# javascript side which works okay without CORS.
#
# from fastapi.middleware.cors import CORSMiddleware
#
# origins = [
#   "http://localhost:3000",
#   "localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


@app.get("/")
async def redirect():
    """Redirect to React app page"""
    return RedirectResponse(url="/app/", status_code=302) 


@app.post("/api/init")
async def handle_init(
    config: Config, settings: Settings, background: BackgroundTasks
) -> None:
    """Initialize the simulation setup"""
    await dispatch.init(config, settings, background)


@app.post("/api/ready")
async def handle_ready(config: Config, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    result = await dispatch.ready(config, settings)
    return result


@app.post("/api/start")
async def handle_start(config: Config, settings: Settings) -> None:
    """Start the simulation"""
    await dispatch.start(config, settings)


@app.get("/api/status")
async def handle_status(config: Config) -> dict:
    """Check the running results of the simulation"""
    result = await dispatch.status(config)
    return result


@app.post("/api/reset")
async def handle_reset(config: Config) -> None:
    """Teardown and reset the simulation"""
    await dispatch.reset(config)
