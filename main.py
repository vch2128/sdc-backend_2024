from fastapi import FastAPI, Query, Path, Body, Cookie, Form, File, UploadFile, HTTPException
from pydantic import BaseModel
from datetime import datetime, time, timedelta
from uuid import UUID
from typing import Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Item_Tag(Item):
    tags: list = []

@app.get("/")
async def root():
    return {
            "message": "Hello World"
            }

# HW3
@app.get("/items/{item_id}")
async def read_items(
                        item_id: Annotated[int, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000")],
                        q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query string must be between 3 and 50 characters")] = None,
                        sort_order: Annotated[str | None, Query()] = "asc"
                    ):
    results = {"item_id": item_id}
    if q:
        results.update({"description": f"This is a sample item that matches the query {q}",
                        "sort_order": sort_order})
    else:
        results.update({"description": "This is a sample item.",
                        "sort_order": sort_order})

    return results


@app.put("/items/{item_id}")
async def update_items(
                item_id: Annotated[int, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000")],
                q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query string must be between 3 and 50 characters")] = None
                ):
    results = {
                "item_id": item_id,
                "name": "Updated Item",
                "description": "Updated item description",
                "price": 20.0,
                "tax": 2.5
                }
    
    if q:
        results.update({"q": q})
    
    return results


# HW4
@app.post("/items/filter/")
async def filter_items(
    price_min: Annotated[float, Query()],
    price_max: Annotated[float, Query()],
    tax_included: Annotated[bool, Query()],
    tags: Annotated[list[str], Query()]
):
    result = {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria."
    }
    
    return result

@app.post("/items/create_with_fields/")
async def create_item_with_fields(
    item: Annotated[Item, Body()],
    importance: Annotated[int, Body()]
):
    result = {
        "item": item,
        "importance": importance
    }
    
    return result

@app.post("/offers/")
async def create_offer(
    name: Annotated[str, Body(description="The name of the offer.")],
    discount: Annotated[float, Body(description="The discount percentage for the offer.")],
    items: Annotated[list[Item], Body(description="A list of items included in the offer.")]
):
    result = {
        "offer_name": name,
        "discount": discount,
        "items": items
    }
    
    return result

@app.post("/users/")
async def create_user(
    username: Annotated[str, Body(description="Username of the user.")],
    email: Annotated[str, Body(description="Email of the user.")],
    full_name: Annotated[str, Body(description="Full name of the user.")]
):
    result = {
        "username": username,
        "email": email,
        "full_name": full_name
    }
    
    return result

@app.post("/items/extra_data_types/")
async def create_item_with_extra_data_types(
    start_time: Annotated[datetime, Body(description="Start time of the item's availability.")],
    end_time: Annotated[time, Body(description="End time of the item's availability.")],
    repeat_every: Annotated[timedelta, Body(description="Time interval for repeating the item.")],
    process_id: Annotated[UUID, Body(description="Unique identifier for the process.")]
):
    result = {
        "message": "This is an item with extra data types.",
        "process_id": process_id
    }
    
    return result

@app.get("/items/cookies/")
async def read_item_with_cookies(
    session_id: Annotated[str, Cookie(description="Session ID from the client's cookies.")] = None
):
    result = {
        "session_id": session_id,
        "message": "This is the session ID obtained from the cookies."
    }

    return result


# HW5
@app.post("/items/form_and_file/")
async def create_item_form_and_file(name: Annotated[str, Form()],
                                    description: Annotated[str | None, Form()],
                                    price: Annotated[float, Form()],
                                    tax: Annotated[float | None, Form()],
                                    file: Annotated[UploadFile, File()]
                                    ):
    if price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")
    
    result = {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax,
        "filename": file.filename,
        "message": "This is an item created using form data and a file."
    }
    
    return result