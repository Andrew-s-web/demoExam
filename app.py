from doctest import master
from typing import Annotated, Optional
from fastapi import FastAPI, Form
import datetime
from pydantic import BaseModel


class OrderItem(BaseModel):
    number: int
    startDate: datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str
    master : Optional[str] = None

class UpdateOrderDTO(BaseModel):
    number : int
    status : Optional[str] = None
    description : Optional[str] = None
    master : Optional[str] = None


repo = [
    OrderItem(
        number = 1,
        startDate = datetime.date(2020, 1, 1),
        device = 'Raspberry Pi',
        problemType = 'CPU',
        description = 'Raspberry Pi fails',
        client = 'Raspberry',
        status = 'Running',
    )
]
app = FastAPI()

@app.get("/orders")
def get_orders():
    return repo
@app.post("/orders")
def create_order(dto : Annotated[OrderItem, Form()]):
    repo.append(dto)
@app.post("/update")
def update_order(dto : Annotated[UpdateOrderDTO, Form()]):
    for o in repo:
        if o.number == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
            if dto.description != "":
                o.description = dto.description
            if dto.master != "":
                o.master = dto.master
            return o
    return "Не найдено"