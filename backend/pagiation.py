from typing import TypeVar

from fastapi import FastAPI, Query
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination.customization import CustomizedPage, UseParamsFields, UseParams,UseResponseHeaders
from fastapi_pagination import Params
from fastapi_pagination.cursor import CursorPage, CursorParams

T = TypeVar("T")

class FoodGramParams(Params):
    size: int = Query(5, ge=1, le=100, alias="pageSize")
    page: int = Query(1, ge=1, alias="pageNumber")


FoodGramPage = CustomizedPage[
    Page[T],
    UseParams(FoodGramParams),
    UseResponseHeaders(
        lambda page: {
            "X-Total-Items": str(page.total),
            "X-Total-Pages": str(page.pages),
        },
    ),
]
