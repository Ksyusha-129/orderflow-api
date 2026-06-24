from fastapi import FastAPI

app = FastAPI(
    title="OrderFlow API",
    description = "REST-сервис учета заказов со статусной машиной",
    version="1.0.0"
)
@app.get("/health")
def health_check():
    return {"status":"ok", "message": "OrderFlow API is running!"}

@app.get("/")
def root():
    return {"message": "Welcome to OrderFlow API!"}
