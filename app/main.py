from fastapi import FastAPI
from app.database import init_db
from app.routers import orders

app = FastAPI(
    title="OrderFlow API",
    description = "REST-сервис учета заказов со статусной машиной",
    version="1.0.0"
)
@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(orders.router, prefix="/orders", tags=["Заказы"])


@app.get("/health")
def health_check():
    return {"status":"ok", "message": "OrderFlow API is running!"}

@app.get("/")
def root():
    return {"message": "Welcome to OrderFlow API!"}
