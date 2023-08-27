import pathlib
from typing import Union
from urllib import response
from fastapi import FastAPI, Depends, HTTPException, Query, Response
from TodosClass import Todos
from sqlmodel import Session, select
import json
from database import TodoModel, engine

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
async def startup_event():
    DATAFILE = pathlib.Path() /'todos.json'
    session = Session(engine)
    
    #Check if database contains database
    stmt = select(TodoModel)
    result = session.exec(stmt).first()
    if result is None:
        with open(DATAFILE,'r') as f:
            the_todos = json.load(f)
            for t in the_todos:
                session.add(TodoModel(**t))
                
        session.commit()
    session.close()
    
  

@app.get('/')
async def get_todos(*,session: Session = Depends(get_session)):
    stmt = select(TodoModel)
    results = session.exec(stmt).all()
    return results


@app.get('/todos/{todo_id}')
async def get_todo(*, session: Session = Depends(get_session),todo_id: int):
        result = session.get(TodoModel,todo_id)
        if result is None:
            response.code = 404
            return {"Status Code":response.code, "Message":f"Todo {todo_id} not found"}
            
        return result
        

@app.post('/todos/',response_model = Todos, status_code=201)
async def create_todos(todo:TodoModel, response:Response, session: Session = Depends(get_session)):
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.put('/todos/{todo_id}', response_model= Union[Todos,str])
async def update_todos(todo_id: int, update_todo: TodoModel, response:Response, session: Session = Depends(get_session)):
    result = session.get(TodoModel,todo_id)
    if result is None:
        response.code = 404
        return {"status code":404,"message":"todo not found"}
    update_data = update_todo.dict(exclude_unset =True)
    print(update_data)
    for k,v in update_data.items():
        setattr(result,k,v)
    session.add(result)
    session.commit()
    session.refresh(result)
    return result

@app.delete("/todos/{todo_id}/")
async def delete_todo(todo_id: int, response:Response, session: Session = Depends(get_session)):
    result = session.get(TodoModel,todo_id)
    if result is None:
        response.code = 404
        return {"status code":404,"message":"todo not found"}
    session.delete(result)
    session.commit()
    return {"message":f"Todo id {todo_id} deleted"}
    
    
