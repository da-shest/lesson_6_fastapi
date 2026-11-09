from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from .repository import OrderRepository
from .service import OrderService
from .config import Settings, get_settings

@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()

def get_service(repository: Annotated[OrderRepository, Depends(get_repository)]) -> OrderService:
    return OrderService(repository)

ServiceDep = Annotated[OrderService, Depends(get_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]