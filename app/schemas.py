from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class OrderStatusEnum(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class OrderCreate(BaseModel):
    client_name: str = Field(..., min_length=2,max_length=100)
    client_email: str
    total_amount: float = Field(default=0, ge=0)

class OrderUpdate(BaseModel):
    client_name: Optional[str] = Field(None, min_length=2, max_length=100)
    client_email: Optional[EmailStr] = None
    total_amount: Optional[float] = Field(None, ge=0)
    status: Optional[OrderStatusEnum] = None


class OrderResponse(BaseModel):
    id: int
    status: str
    client_name: str
    client_email: str
    total_amount: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True