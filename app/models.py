from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class OrderStatus(str, enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.DRAFT,nullable=False)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=False)
    total_amount = Column(Numeric(10,2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable = False)

    def __repr__(self):
        return f"<Order(id={self.id}, status={self.status}, client ={self.client_name})>"