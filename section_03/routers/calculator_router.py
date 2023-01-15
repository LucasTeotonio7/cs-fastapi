from fastapi import APIRouter
from fastapi import Query, Header
from typing import Any, Dict, List, Optional
from docs.calculator import *

router = APIRouter(
    tags=["Calculator"]
)


@router.get('/calculator', **get_calculator_doc)
async def calculate(
    a: int = Query(default=0, gt=5), 
    b: int = Query(default=0, gt=10),
    x_geek: str = Header(default=None),
    c: Optional[int]=0):

    print(f'X_GEEK {x_geek}')

    result = a + b + c
    return {"result": result}
