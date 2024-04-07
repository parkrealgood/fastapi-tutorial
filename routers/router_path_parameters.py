from enum import Enum
from typing import Union

from fastapi import APIRouter

router = APIRouter()


"""
    Summary
    
    FastAPI를 이용하면 짧고 직관적인 표준 파이썬 타입 선언을 사용하여 다음을 얻을 수 있습니다:
    1. 편집기 지원: 오류 검사, 자동완성 등
    2. 데이터 파싱
    3. 데이터 검증
    4. API 주석(Annotation)과 자동 문서
"""


# 경로 매개변수 & 선택적 매개변수
@router.get("/items/{item_id}")
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
@router.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    one = "one"
    two = "two"
    three = "three"


# enum 사용
@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # 열거형 멤버 비교
    if model_name is ModelName.one:
        return {"model_name": model_name, "message": "one!"}
    # 열거형 값 가져오기
    if model_name.value == "two":
        return {"model_name": model_name, "message": "two!"}

    return {"model_name": model_name, "message": "three!"}


# 경로 변환
@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
