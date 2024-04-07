from fastapi import FastAPI

from routers.router_path_parameters import router as path_parameters_router
from routers.router_query_parameters import router as query_parameters_router
from routers.router_request_body import router as request_body_router
from routers.router_post_request_body import router as post_request_body_router

app = FastAPI()  # FastAPI 인스턴스 생성

app.include_router(path_parameters_router)
app.include_router(query_parameters_router)
app.include_router(request_body_router)
app.include_router(post_request_body_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
