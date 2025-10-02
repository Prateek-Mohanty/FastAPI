from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user/get_user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['user_name'] == 'codingwithmetest'
    assert response.json()['email'] == 'codingwithmetest@email.com'
    assert response.json()['first_name'] == 'Prateek'
    assert response.json()['last_name'] == 'Mohanty'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '8249314252'

def test_change_password_success(test_user):
    changed_password = {
        'password':'testpassword',
        'new_password':'testpassword1'
    }
    response = client.put('/user/change_password', json = changed_password)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_changed_password_invalid_password(test_user):
    changed_password = {
        'password':'something',
        'new_password':'testpassword1'
    }
    response = client.put('/user/change_password', json = changed_password)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Password Mismatch'}

def test_change_phone_number(test_user):
    response = client.put('/user/update_phone_number/{9040014252}')
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSession()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model.phone_number == model.phone_number