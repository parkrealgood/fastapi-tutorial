from typing import Union, Set, List, Dict

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Post(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: Union[List[Image], None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    posts: List[Post]


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@router.put("/posts/{post_id}")
async def update_post(
        post_id: int,
        post: Post,
        user: User,
        importance: int = Body(gt=0),
):
    results = {"post_id": post_id, "post": post, "user": user, "importance": importance}
    return results


@router.put("/posts/{post_id}/single")
async def update_single_post(post_id: int, post: Post = Body(embed=True)):
    results = {"post_id": post_id, "post": post}
    return results


@router.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@router.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


@router.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights