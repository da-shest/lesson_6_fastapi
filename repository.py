class OrderRepository:
    def __init__(self):
        self._orders = []

    def get_all(self) -> list[dict]:
        return self._orders

    def _get_order_idx(self, order_id: int) -> int | None:
        for idx, order in enumerate(self._orders):
            if order['id'] == order_id:
                return idx

    def get_by_id(self, order_id: int) -> dict | None:
        idx = self._get_order_idx(order_id)
        if idx is not None:
            return self._orders[idx]

    def add(self, order: dict) -> dict:
        order["id"] = len(self._orders) + 1
        self._orders.append(order)
        return order

    def delete(self, order_id: int) -> dict | None:
        idx = self._get_order_idx(order_id)
        if idx is not None:
            self._orders.pop(idx)
            return {}

    def update(self, order_id, update_data) -> dict | None:
        idx = self._get_order_idx(order_id)
        if idx is not None:
            self._orders[idx] = update_data
            return {}
    