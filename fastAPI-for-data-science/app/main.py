import contextlib

from .routers import temparature, http, post
from .internal.database import create_all_tables, seed_posts
from fastapi import FastAPI


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    await seed_posts()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(temparature.router)
app.include_router(http.router)

app.include_router(post.router)
