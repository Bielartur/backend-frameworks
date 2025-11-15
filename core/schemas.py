from ninja import Schema
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class ErrorSchema(Schema):
    error: str


class BaseResponse(Schema, Generic[T]):
    message: str
    data: Optional[T] = None
