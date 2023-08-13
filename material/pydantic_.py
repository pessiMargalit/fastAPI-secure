# Pydantic:
#     - data classes in python and a word about static typing
from enum import Enum

from pydantic import BaseModel, field_validator, model_validator, conint, \
    conlist, computed_field
from typing import Union, Optional


class Category(Enum):
    FRUITS = 1
    VEGGIES = 2
    DAIRY = 3


class Product(BaseModel):
    name: str
    price: conint(ge=0, lt=100)
    stock: conint(ge=0) = 20
    exp_date: Optional[str] = None
    manufacture_date: Optional[str] = None
    category: Category

    @field_validator("exp_date")
    def exp_date_is_not_today(cls, exp_date):
        print("Validating experation date")
        if exp_date != "17/07/2023":
            return exp_date + "!"
        raise ValueError("Product is bad")

    @computed_field
    @property
    def nutritions(self) -> str:
        if self.category == Category.DAIRY:
            return "Nope"
        return "Very healthy"

    # @field_validator("price", "stock")
    # def validate_non_negative(cls, num):
    #     if num < 0:
    #         raise ValueError("Value cannot be negative")
    #     return num

    @model_validator(mode="before")
    def validate_exp_or_manufacture(cls, values):
        print("Validating both exp and man")
        if values.get("exp_date") or values.get("manufacture_date"):
            return values
        raise ValueError("Item must contain exp_date or manufacture_date")


#     - basic automatic validation (type conversion, optional, default values)
p1 = Product(name="Apple", price="34", exp_date="19/07/2023", stock=16, category=Category.FRUITS)
p2 = Product(name="Onion", price=15, category=Category.VEGGIES, manufacture_date="19/07/2022", stock=20)
print(p1)
print(p2)

product3_dict = {
    "exp_date": "18/07/2023",
    "price": 30,
    "name": "Milk",
    "category": Category.DAIRY
}

p3 = Product(**product3_dict)
print(p3)

p3.category = Category.FRUITS
print(p3)
print(p3.nutritions)


#     - enum
#     - @pydantic.feild_validator() (single prop, multiple props)
#     - @pydantic.model_validator
#     - unpack dict (ex: from json)
#     - conint, constr, conlist

class Store(BaseModel):
    name: str
    items: conlist(Product, max_length=1000)


#     - updating an instance
#     - @computed_field
#     - Show in fastapi (a word about fastapi's dark magic)


import uvicorn
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def sanity():
    return "OK"


@app.post("/store/item")
async def add_product(product: Product):
    print(product)
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, timeout_keep_alive=0)
