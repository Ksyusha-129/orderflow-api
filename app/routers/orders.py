from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Order, OrderStatus
from app.schemas import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Создать новый заказ"""
    db_order = Order (
        client_name=order_data.client_name,
        client_email=order_data.client_email,
        total_amount = order_data.total_amount,
        status=OrderStatus.DRAFT
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список заказов"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Получить заказ по ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

ALLOWED_TRANSITIONS = {
    "draft": ["confirmed", "cancelled"],
    "confirmed": ["processing"],
    "processing": ["shipped", "cancelled"],
    "shipped": ["delivered"],
    "delivered": [], #Из статуса "Доставлен" нельзя перейти в др статусы
    "cancelled": []
}

@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.status:
        current_status = db_order.status.value
        new_status = order_update.status

        allowed_next_statuses = ALLOWED_TRANSITIONS.get(current_status, [])

        if new_status not in allowed_next_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition: from '{current_status}' to '{new_status.value}'. Allowed: {allowed_next_statuses}"
            )
        

    update_data = order_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", status_code=204)
def delete_order(order_id:int, db: Session = Depends(get_db)):

    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail ="Order not found")
    
    if db_order.status not in [OrderStatus.DRAFT, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete order with status '{db_order.status.value}'. Only draft or cancelled orders can be deleted."
        )
    db.delete(db_order)
    db.commit()

    return None