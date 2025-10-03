from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "DevMate running!"}

@app.get("/health")
def health():
    return {"status": "ok"}
