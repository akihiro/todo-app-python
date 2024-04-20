from fastapi import FastAPI, HTTPException

from .database import lifespan, async_session, Item


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"msg": "hello world"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.get(Item, item_id)
        if item is None:
            item = Item(id=item_id, counter=1)
            raise HTTPException(status_code=404, detail="Item not found")
        await session.commit()
    return item


@app.post("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    async with async_session() as session:
        item = await session.get(Item, item_id)
        if item is None:
            item = Item(id=item_id, counter=1)
        else:
            item.counter += 1
        session.add(item)
        await session.commit()
    return item
