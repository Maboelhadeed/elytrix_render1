from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Elytrix API running."}

@app.get("/run")
def run(strategy: str, mode: str):
    return {"message": f"Strategy {strategy} running in {mode} mode."}
