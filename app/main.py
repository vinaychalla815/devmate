from fastapi import FastAPI
from .routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DevMate running!"}

app.include_router(router)
