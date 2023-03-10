from fastapi import FastAPI, Query, Path
from enum import Enum

from typing import Union

from pydantic import BaseModel, Required

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
'''

@app.get("/users/me")
async def read_user_me():
    return {"user_id" : "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users")
async def read_users():
    return ["rick", "morty"]

@app.get("/users")
async def read_users():
    return ["Bean", "Elfo"]


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name" : model_name, "message" : "Deep Learnging FTW!"}
    if model_name.value == "lenet":
        return {"model_name" : model_name, "message" : "LeCNN all the images"}
    return {"model_name" : model_name, "message" : "Have some residuals"}

@app.get("/files/{file_path:path")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
'''
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
'''
@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=..., title="Query string", description="Query string for the items to serach in the databsae that have a good match", min_length=3, max_length=50, regex="^fixedquery$")):
#async def read_items(q: Union[str, None] = Query(default=Required, alias="item-query", deprecated=True, min_length=3, include_in_schema=False)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
'''
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description" : "This is an amazing item that has a long description"}
        )
    return item
'''
@app.get("/items/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get", gt=0, le=1000), q:str, size: float = Query(gt=0, lt=10.5)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
        results.update({"size": size})
    return results

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id:str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/items/{item_id")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item.dict

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id":item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result