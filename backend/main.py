from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to GIMES Backend"
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "GIMES Backend"
    }