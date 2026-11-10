from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .dependencies import get_repository, SettingsDep
from .exceptions import OrderNotFoundError, OrderAlreadyCompletedError
from .routers import orders

app = FastAPI(
    title="Сервис заказа напитков",
    description="API для управления заказами, фильтрации и получения информации.",
    version="1.0.0",
    contact={"name": "Поддержка API", "email": "support@aboba.ru"},
    license_info={"name": "MIT License"},
)

app.include_router(orders.router)


@app.exception_handler(OrderNotFoundError)
async def handle_order_not_found(request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Заказ с id={exc.order_id} не найден"},
    )


@app.exception_handler(OrderAlreadyCompletedError)
async def handle_order_completed(request, exc: OrderAlreadyCompletedError):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Заказ {exc.order_id} уже выполнен и не может быть изменён"},
    )


@app.get('/', tags=["Сервис"], summary='Приветственное сообщение в корне')
async def read_root():
    return {'message': 'Добро пожаловать в сервис заказов!'}


@app.get('/info', tags=["Сервис"],
         summary='Информация о названии и количестве заказов')
async def get_inf(settings: SettingsDep):
    return {
        'app_name': settings.app_name,
        'orders_count': len(get_repository().get_all()),
    }