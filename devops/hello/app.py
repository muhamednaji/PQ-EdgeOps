from fastapi import FastAPI
app = FastAPI(title="hello-service")

@app.get("/health")
def health():
    return {"status": "ok"}
