from fastapi import FastAPI
from .Api import router

app = FastAPI()
app.include_router(router)
