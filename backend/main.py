#FastAPI app. what starts my api server (uvicornn main : app)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Starbleep backend is running"}