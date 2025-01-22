from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def root():
    return {
            "message": "Hello World"
            }


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