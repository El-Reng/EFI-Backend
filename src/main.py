from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from . import models
from .routers import users, categories, products

app = FastAPI()

app.title = "API - EFI Backend"
app.summary = "Por Acuña, Rojo y Roldan"

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.users_router, prefix="/users")
app.include_router(categories.categories_router, prefix="/categories")
app.include_router(products.products_router, prefix="/products")

add_pagination(app)
