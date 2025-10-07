from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app import routes

app = FastAPI(title="DevMate AI Backend")

# Mount static folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root route to serve the HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("app/static/index.html", "r") as f:
        return f.read()

# Include API routes
app.include_router(routes.router)
