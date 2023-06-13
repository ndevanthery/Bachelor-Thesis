# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder

import json


app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["POST", "GET", "PUT"],
    allow_headers=["*"],
)


class BillLine(BaseModel):
    code: str | None = None
    description: str | None = None


class Item(BaseModel):
    title: str | None = None
    date: str | None = None
    status: str | None = None
    report: str | None = None
    bill: list[BillLine] = []


f = open('reports.json', encoding='utf-8')

# returns JSON object as
# a dictionary
data = json.load(f)

f.close()


@app.get("/", response_model=list[Item])
async def root():
    return data


@app.get("/length")
async def get_length():

    return len(data)


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id):

    return data[int(item_id)]


@app.put("/status/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    data[item_id]["status"] = item.status

    json_string = json.dumps(data, indent=4)
    with open('reports.json', 'w') as outfile:
        outfile.write(json_string)

    return data[item_id]
