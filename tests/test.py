from datetime import date
from typing import Annotated

from fastapi import Header, HTTPException
from fastapi.testclient import TestClient

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base, Task, TaskStatus
from db import get_db
from main import app, verify_token

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    db_task = Task(
        id=1,
        title='Task1',
        description='testing tests',
        due_date=date(2025, 5, 19),
        status=TaskStatus.NEW
    )
    session.add(db_task)
    session.commit()
    session.close()

    yield session

    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

TEST_TOKEN = 'sometoken'


def verify_test_token(x_token: Annotated[str, Header()]):
    if x_token != TEST_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.dependency_overrides[verify_token] = verify_test_token


def test_get_list():
    response = client.get(
        '/',
        headers={'X-Token': TEST_TOKEN})
    assert response.status_code == 200


def test_get_task():
    task_id = 1
    response = client.get(
        f'task/{task_id}',
        headers={'X-Token': TEST_TOKEN},
    )

    assert response.status_code == 200, response.text
    task = response.json()
    assert task['title'] == 'Task1'
    assert task['description'] == 'testing tests'
    assert task['due_date'] == '2025-05-19'
    assert task['status'] == 'NEW'


def test_create_task():
    response = client.post(
        "create",
        headers={'X-Token': TEST_TOKEN},
        json={"title": "Test", "description": "Some text", "due_date": "2025-06-26", "status": "IN_PROGRESS"}
    )
    assert response.status_code == 201, response.text
    task = response.json()
    assert task is not None
    assert task['title'] == "Test"
    assert task['description'] == "Some text"
    assert task['due_date'] == '2025-06-26'
    assert task['status'] == "IN_PROGRESS"


def test_update():
    task_id = 1
    response = client.patch(
        f"update/{task_id}",
        headers={'X-Token': TEST_TOKEN},
        json={'status': 'DONE'}
    )

    assert response.status_code == 200, response.text
    task = response.json()
    assert task['status'] == 'DONE'


def test_delete():
    task_id = 1
    response = client.delete(f'delete/{task_id}', headers={'X-Token': TEST_TOKEN})
    assert response.status_code == 200, response.text
    task = response.json()
    assert task['id'] == task_id
    response = client.get(f'task/{task_id}', headers={'X-Token': TEST_TOKEN})
    assert response.status_code == 404

