from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from .repository import OrderRepository
from .service import OrderService
from .config import Settings, get_settings


@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()


def get_service(
    repository: Annotated[OrderRepository, Depends(get_repository)],
) -> OrderService:
    return OrderService(repository)


def pagination_params(
    settings: Annotated[Settings, Depends(get_settings)],
    limit: int | None = None,
    offset: int | None = None,
) -> tuple[int, int]:
    if limit is None:
        limit = settings.default_page_size
    elif limit > settings.max_page_size:
        limit = settings.max_page_size
    if offset is None:
        offset = settings.default_offset
    return limit, offset


ServiceDep = Annotated[OrderService, Depends(get_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
PaginationDep = Annotated[tuple[int, int], Depends(pagination_params)]