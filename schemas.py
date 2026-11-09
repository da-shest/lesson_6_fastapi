from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class DrinkSize(str, Enum):
    small = 'small'
    medium = 'medium'
    large = 'large'

class OrderStatus(str, Enum):
    pending = 'pending'
    ready = 'ready'
    completed = 'completed'

class OrderCreate(BaseModel):
    drink: str = Field(min_length=1, max_length=100, description="Название напитка из меню", examples=["Капучино"])
    size: DrinkSize = Field(description="Размер порции", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество порций", examples=[2])
    customer_name: str | None = Field(default=None, min_length=1, max_length=100, description="Имя клиента", examples=["Алексей"])

class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1, max_length=100, description="Новое название напитка", examples=["Латте"])
    size: DrinkSize | None = Field(default=None, description="Новый размер", examples=["large"])
    quantity: int | None = Field(default=None, gt=0, description="Новое количество", examples=[1])
    customer_name: str | None = Field(default=None, min_length=1, max_length=100, description="Новое имя клиента", examples=["Ольга"])
    status: OrderStatus | None = Field(default=None, description="Новый статус заказа", examples=["ready"])

class Order(OrderCreate):
    id: int = Field(description="Уникальный идентификатор заказа", examples=[1])
    status: OrderStatus = Field(default='pending', description="Текущий статус заказа", examples=["pending"])
    created_at: datetime = Field(description="Метка времени создания", examples=["2026-03-30T12:00:00"])