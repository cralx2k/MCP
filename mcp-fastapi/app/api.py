from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import ItemModel

app = FastAPI(title="MCP Template API")

Base.metadata.create_all(bind=engine)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


class Item(BaseModel):
    name: str
    description: str


class ItemResponse(Item):
    id: int
    model_config = ConfigDict(from_attributes=True)


@app.get("/items", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", status_code=201, response_model=ItemResponse)
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = ItemModel(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.post("/items/{item_id}/clone", response_model=ItemResponse)
def clone_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    cloned_item = ItemModel(
        name=item.name + " (clone)",
        description=item.description,
    )
    db.add(cloned_item)
    db.commit()
    db.refresh(cloned_item)
    return cloned_item


@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item
