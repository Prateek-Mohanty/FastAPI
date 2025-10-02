from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
import pytest
from models import Todos, Users
from routers.auth import bcrypt_context

DATABASE_URL = 'sqlite:///./testdb.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False})
TestingSession = sessionmaker(autoflush=False, autocommit=False, bind = engine)
Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'codingwithmetest','id':1,'user_role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description = "Need to learn everyday",
        priority = 5,
        complete = False,
        owner_id = 1
    )

    db = TestingSession()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todosapp;"))
        connection.commit()

@pytest.fixture
def test_user():

    user = Users(
        user_name = 'codingwithmetest',
        email = 'codingwithmetest@email.com',
        first_name = 'Prateek',
        last_name = 'Mohanty',
        hashed_password = bcrypt_context.hash('testpassword'),
        phone_number = '8249314252',
        role = 'admin'
    )

    db = TestingSession()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('delete from users;'))
        connection.commit()
