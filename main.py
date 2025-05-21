from datetime import date
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Header, status, Response
from sqlalchemy.orm import Session

from schemas import StatusEnum
import schemas
from db import get_db
from models import Task


app = FastAPI()


AUTHORIZATION_TOKEN = 'jfeoiajeofj'


def verify_token(x_token: Annotated[str, Header()]):
    if x_token != AUTHORIZATION_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


def get_task_or_404(pk: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == pk).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task


@app.get('/', dependencies=[Depends(verify_token)], status_code=status.HTTP_200_OK)
def tasks_list(db: Session = Depends(get_db),
               tasks_status: StatusEnum | None = None,
                            from_date: date | None = None, to_date: date | None = None):
    q = db.query(Task)
    if tasks_status:
        q = q.filter(Task.status == tasks_status)

    if from_date:
        q = q.filter(Task.due_date >= from_date)

    if to_date:
        q = q.filter(to_date >= Task.due_date)
    return q.all()


@app.get('/task/{pk}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
def get_task(pk: int, db: Session = Depends(get_db)):
    return get_task_or_404(pk, db)


@app.post('/create', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def create(task_schema: schemas.TaskBase, db: Session = Depends(get_db)):
    new_task = Task(title=task_schema.title, description=task_schema.description, due_date=task_schema.due_date,
                    status=task_schema.status)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.patch('/update/{pk}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
def update(pk: int, task_schema: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = get_task_or_404(pk, db)
    task_data = task_schema.model_dump(exclude_unset=True)
    db.query(Task).filter(Task.id == pk).update(task_data)
    db.commit()
    db.refresh(task)
    return task


@app.delete('/delete/{pk}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
def destroy(pk: int, db: Session = Depends(get_db)) -> Response:
    task = get_task_or_404(pk, db)
    db.delete(task)
    db.commit()
    return task
