from fastapi import APIRouter, status, Response
from ..dependencies import ServiceDep, PaginationDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED,
             summary='Создание заказа')
def create_order(order: OrderCreate, service: ServiceDep):
    return service.create_order(order)


@router.get("", response_model=list[Order], summary='Получение списка заказов')
def list_orders(service: ServiceDep, pagination: PaginationDep,
                status: OrderStatus | None = None):
    limit, offset = pagination
    return service.list_orders(limit, offset, status)


@router.get("/{order_id}", response_model=Order, summary='Получение заказа по ID')
def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)


@router.patch("/{order_id}", response_model=Order,
              summary='Внесение изменений в заказ по ID')
def edit_order(order_id: int, order_update: OrderUpdate, service: ServiceDep):
    update_data = order_update.model_dump(exclude_unset=True)
    return service.update_order(order_id, update_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary='Удаление заказа по ID')
def delete_order(order_id: int, service: ServiceDep):
    service.delete_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)