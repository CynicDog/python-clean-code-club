from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users, temparature, http, post


app = FastAPI()

app.include_router(
    users.router,
    dependencies=[Depends(get_query_token)]
)
app.include_router(
    items.router,
    dependencies=[Depends(get_query_token)]
)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(temparature.router)

app.include_router(http.router)

app.include_router(
    post.router,
)