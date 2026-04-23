from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.routes import drivers, loads, dispatch

app = FastAPI(
    title="Pedal to the Metal",
    description="Dispatch SaaS for concrete fleet managers. Built by a dispatcher, for dispatchers.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drivers.router, prefix="/api")
app.include_router(loads.router, prefix="/api")
app.include_router(dispatch.router, prefix="/api")

# Serve frontend static files if they exist
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")


@app.get("/health")
def health():
    return {"status": "ok", "service": "pedal-to-the-metal"}


@app.get("/")
def root():
    return {"message": "Pedal to the Metal API v0.1 — see /docs for endpoints"}
