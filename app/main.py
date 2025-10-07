from fastapi import FastAPI
from app import routes

app = FastAPI(title="DevMate AI Backend")

# connect all routes from routes.py
app.include_router(routes.router)
