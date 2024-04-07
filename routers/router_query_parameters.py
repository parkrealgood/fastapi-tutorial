from typing import Union, List

from fastapi import APIRouter, Query, Path

router = APIRouter()

"""
    Summary

    매개변수에 검증과 메타데이터를 추가 선언할 수 있습니다.
    1. 제네릭 검증과 메타데이터:
        - alias
        - title
        - description
        - deprecated

    2. 특정 문자열 검증:
        - min_length
        - max_length
        - regex
        
    3. 숫자 검증:
        - gt: 크거나(greater than)
        - ge: 크거나 같은(greater than or equal)
        - lt: 작거나(less than)
        - le: 작거나 같은(less than or equal)
"""


# 여러 경로/쿼리 매개변수
@router.get("/users/{user_id}/items/{item_id}")
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


# 쿼리 매개변수와 문자열 검증
@router.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 쿼리 매개변수 리스트 / 다중값
@router.get("/item-list/")
async def read_item_lists(q: Union[List[str], None] = Query(
    default=None, title="Query string", description="description"
)
):
    query_items = {"q": q}
    return query_items


# alias / deprecated
@router.get("/deprecated-items/")
async def read_items(q: Union[str, None] = Query(
    default=None, alias="item-query", deprecated=True
)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 숫자검증
@router.get("/post/{post_id}")
async def read_posts(
        *,
        post_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
        q: str,
        size: float = Query(gt=0, lt=10.5),
):
    results = {"post_id": post_id}
    if q:
        results.update({"q": q})
    return results
