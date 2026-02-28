from fastapi import FastAPI
from .router import iris


app = FastAPI(title = "Iris Inference API",)

app.include_router(iris.router)
