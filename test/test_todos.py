from starlette import status
from models import Todos
from routers.todos import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/todos/get_all')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,'description':"Need to learn everyday",'title':"Learn to code",'priority':5,'owner_id':1,'id':1}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete':False,'description':"Need to learn everyday",'title':"Learn to code",'priority':5,'owner_id':1,'id':1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Does not exist on database'}

def test_create_todo(test_todo):
    response_data = {
        'title':'New Todo!',
        'description':'New todo created',
        'priority':5,
        'complete':False
    }
    response = client.post('/todos/create_todo', json = response_data)
    assert response.status_code == 201

    db = TestingSession()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == response_data.get('title')
    assert model.description == response_data.get('description')
    assert model.priority == response_data.get('priority')

def test_change_todo(test_todo):
    changed_todo =  {
        'title':'Change the description!',
        'description':'Need to learn everyday',
        'priority':5,
        'complete':False
    }

    response = client.put('/todos/1', json = changed_todo)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestingSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == changed_todo.get('title')
    assert model.description == changed_todo.get('description')
    assert model.priority == changed_todo.get('priority') 
    assert model.complete == changed_todo.get('complete')

def test_change_todo_not_found(test_todo):
    changed_todo =  {
        'title':'Change the description!',
        'description':'Need to learn everyday',
        'priority':5,
        'complete':False
    }

    response = client.put('/todos/999', json = changed_todo)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Request not found.'}    

def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_notfound(test_todo):
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    db = TestingSession()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert response.json() == {'detail':'Todo not found.'}
    