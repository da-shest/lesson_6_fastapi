from datetime import datetime
from .repository import OrderRepository
from .exceptions import OrderNotFoundError, OrderAlreadyCompletedError
from .schemas import OrderStatus


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def list_orders(self, limit: int, offset: int, status: OrderStatus | None) -> list[dict]:
        result = self.repository.get_all()
        if status is not None:
            result = [o for o in result if o["status"] == status]
        return result[offset: offset + limit]

    def get_order(self, order_id: int) -> dict:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def create_order(self, data) -> dict:
        payload = data.model_dump()
        payload["status"] = OrderStatus.pending
        payload["created_at"] = datetime.now()
        return self.repository.add(payload)

    def update_order(self, order_id: int, update_data: dict) -> dict:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        if order["status"] == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)
        return self.repository.update(order_id, update_data)

    def delete_order(self, order_id: int) -> None:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        if order["status"] == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)
        self.repository.delete(order_id)