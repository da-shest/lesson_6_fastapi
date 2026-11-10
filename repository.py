class OrderRepository:
    def __init__(self):
        self._orders: list[dict] = []
        self._next_id = 1

    def get_all(self) -> list[dict]:
        return self._orders

    def get_by_id(self, order_id: int) -> dict | None:
        for order in self._orders:
            if order["id"] == order_id:
                return order
        return None

    def add(self, order: dict) -> dict:
        new_order = dict(order)
        new_order["id"] = self._next_id
        self._next_id += 1
        self._orders.append(new_order)
        return new_order

    def update(self, order_id: int, update_data: dict) -> dict | None:
        order = self.get_by_id(order_id)
        if order is None:
            return None
        order.update(update_data)
        return order

    def delete(self, order_id: int) -> dict | None:
        for idx, order in enumerate(self._orders):
            if order["id"] == order_id:
                return self._orders.pop(idx)
        return None