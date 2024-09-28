from fastapi import FastAPI, Query, Path
from typing import Annotated

app = FastAPI()


@app.get("/")
async def root():
    return {
            "message": "Hello World"
            }


@app.put("/items/{item_id}")
async def read_items(
                        item_id: Annotated[int, Path()],
                        q: Annotated[str | None, Query()] = None
                    ):
    results = {
                "item_id": item_id,
                "name": "Test Item",
                "description": "A test description",
                "price": 10.5,
                "tax": 1.5
                }
    if q:
        results.update({"q": q})

    return results
