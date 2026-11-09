from fastapi import FastAPI, Depends, status, HTTPException, Response
from typing import Annotated
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from enum import Enum

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
    # drink: str
    # size: DrinkSize
    # quantity: int
    # customer_name: str | None
    status: OrderStatus = Field(default='pending', description="Текущий статус заказа", examples=["pending"])
    created_at: datetime = Field(description="Метка времени создания", examples=["2026-03-30T12:00:00"])

class Settings(BaseSettings):
    app_name: str = 'ABOBA'
    default_page_size: int = 15
    max_page_size: int = 60
    default_offset: int = 0

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

app = FastAPI(
    title="Сервис заказа напитков",
    description="API для управления заказами, фильтрации и получения информации.",
    version="1.0.0",
    contact={
        "name": "Поддержка API",
        "email": "support@aboba.ru",
    },
    license_info={
        "name": "MIT License",
    },
)

orders_db = []
order_counter = 0

@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=Order, tags=["Заказы"], summary='Создание заказа')
async def create_order(order: OrderCreate):
    new_order = order.model_dump()
    global order_counter
    order_counter += 1
    new_order['id'] = order_counter
    new_order['status'] = 'pending'
    new_order['created_at'] = datetime.now()
    orders_db.append(new_order)
    return new_order

@app.get('/orders', tags=["Заказы"], summary='Получение списка заказов')
async def list_orders(settings: SettingsDep, limit: int | None = None, offset: int | None = None, status: OrderStatus | None = None):
    if limit is None:
        limit = settings.default_page_size
    elif limit > settings.max_page_size:
        limit = settings.max_page_size
    if offset is None:
        offset = settings.default_offset
    result = orders_db
    if status is not None:
        result = [o for o in result if o['status'] == status]
    return result[offset : offset + limit]

@app.get('/orders/{order_id}', response_model=Order, tags=["Заказы"], summary='Получение заказа по ID')
async def get_order(order_id: int):
    for order in orders_db:
        if order['id'] == order_id:
            return order
    raise HTTPException(status_code=404, detail='Заказ не найден')

@app.patch('/orders/{order_id}', response_model=Order, tags=["Заказы"], summary='Внесение изменений в заказ по ID')
async def edit_order(order_id: int, order_update: OrderUpdate):
    target_order = None
    for order in orders_db:
        if order['id'] == order_id:
            target_order = order
    if target_order is None:
        raise HTTPException(status_code=404, detail='Заказ не найден')
    update_data = order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        target_order[field] = value
    return target_order

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Заказы"], summary='Удаление заказа по ID')
async def delete_order(order_id: int):
    global orders_db
    db_len = len(orders_db)
    orders_db = [o for o in orders_db if o['id'] != order_id]
    if db_len == len(orders_db):
        raise HTTPException(status_code=404, detail='Заказ не найден')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get('/', tags=["Сервис"], summary='Приветственное сообщение в корне')
async def read_root():
    return {'message': 'Добро пожаловать в сервис заказов!'}

@app.get('/info', tags=["Сервис"], summary='Информация о названии и количестве заказов')
async def get_inf(settings: SettingsDep):
    return {'app_name': settings.app_name, 'orders_count': len(orders_db)}
