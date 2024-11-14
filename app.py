from fastapi import FastAPI
import datetime
from pydantic import BaseModel


class OrderItem(BaseModel):
    number: int
    startDate: datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status: str

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