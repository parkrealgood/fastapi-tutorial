from enum import Enum
from typing import Union

from fastapi import FastAPI  # FastAPI를 통해 api 제공
from pydantic import BaseModel


app = FastAPI()  # FastAPI 인스턴스 생성


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 경로 매개변수 & 선택적 매개변수
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# /users/{user_id}와 /users/me 두 경로가 겹치는데, FastAPI는 먼저 선언된 경로가 먼저 매칭된다.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    one = "one"
    two = "two"
    three = "three"


# enum 사용
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # 열거형 멤버 비교
    if model_name is ModelName.one:
        return {"model_name": model_name, "message": "one!"}
    # 열거형 값 가져오기
    if model_name.value == "two":
        return {"model_name": model_name, "message": "two!"}

    return {"model_name": model_name, "message": "three!"}


# 경로 변환
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# 쿼리 매개 변수
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# 여러 경로/쿼리 매개변수
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# 요청 본문
# 데이터 모델
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 모델 사용하기
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# 요청 본문 + 경로 매개변수 + 쿼리 매개변수
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
