from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# 요청 본문
# 데이터 모델
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 모델 사용하기
@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 요청 본문 + 경로 매개변수 + 쿼리 매개변수
@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
