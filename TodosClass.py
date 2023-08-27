from pydantic import BaseModel
from typing import Union


class Todos(BaseModel):
    id: int
    description: Union[str, None] = None
