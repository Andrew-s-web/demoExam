from typing import Annotated, Optional, List
from fastapi import FastAPI, Form
import datetime
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware


class OrderItem(BaseModel):
    number: int
    startDate: datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str
    master : Optional[str] = None
    comments : List[str] = Field(default_factory=list)

class UpdateOrderDTO(BaseModel):
    number : int
    status : Optional[str] = None
    description : Optional[str] = None
    master : Optional[str] = None
    comment : Optional[str] = None


repo = [
    OrderItem(
        number = 1,
        startDate = datetime.date(2020, 1, 1),
        device = 'Raspberry Pi',
        problemType = 'CPU',
        description = 'Raspberry Pi fails',
        client = 'Raspberry',
        status = 'Running',
    ),
    OrderItem(
        number = 2,
        startDate = datetime.date(2020, 1, 1),
        device = 'Raspberry Pi',
        problemType = 'CPU',
        description = 'Raspberry Pi fails',
        client = 'Raspberry',
        status = 'Running',
    ),
    OrderItem(
        number = 3,
        startDate = datetime.date(2020, 1, 1),
        device = 'Raspberry Pi',
        problemType = 'CPU',
        description = 'Raspberry Pi fails',
        client = 'Raspberry',
        status = 'Running',
    )
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

message = ''

@app.get("/orders")
def get_orders(param=None):
    global message
    buffer = message
    if param:
        return {'repo': [o for o in repo if o.number == int(param)], "message": buffer}
    return {'repo': repo, "message": buffer}

@app.post("/orders")
def create_order(dto : Annotated[OrderItem, Form()]):
    repo.append(dto)

@app.post("/update")
def update_order(dto : Annotated[UpdateOrderDTO, Form()]):
    global message
    for o in repo:
        if o.number == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
                message += f"Статус заявки №{o.number} изменен\n"
                if o.status.lower() == "выполнено":
                    message += f"Заявка №{o.number} завершена\n"
            if dto.description != "":
                o.description = dto.description
            if dto.master != "":
                o.master = dto.master
            if dto.comment != None and dto.comment != "":
                o.comments.append(dto.comment)
            return o
    return "Не найдено"
