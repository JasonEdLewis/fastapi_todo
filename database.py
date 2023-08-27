from typing import Optional
from sqlmodel import SQLModel,Field, create_engine

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

class TodoModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    

def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()