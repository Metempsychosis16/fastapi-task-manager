from fastapi.testclient import TestClient
import uuid

from app.main import app

client=TestClient(app)




def test_health():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()=={
            "status":"running"
            }


def test_register():

    random_email=f"{uuid.uuid4()}@gmail.com"

    response=client.post("/api/register",json={
        "email":random_email,"password":"123456"
        }

                         )
    print(response.json())
    assert response.status_code==201


def test_login():
    response=client.post("/api/login",json={
        "email":"test@gmail.com",
        "password":"123456"
        }
                         )

    assert response.status_code==200
    data=response.json()
    assert "access_token"in data

def test_protected_route():
    random_email = f"{uuid.uuid4()}@gmail.com"    

    client.post("/api/register",json={"email":random_email,"password":"123456"})
    login_response=client.post("/api/login",json={

        "email":random_email,"password":"123456"
        })
   
    print(login_response.json())

    token =login_response.json()["access_token"]


    headers={
        "Authorization" : f"Bearer {token}"

        }

    response=client.get("/api/tasks",headers=headers)


def test_invalid_login():

    response=client.post("/api/login",json={
        "email":"wrong@gmail.com","password":"123456"

        })
                         

    assert response.status_code==401


def test_create_task():
     login_response=client.post("/api/login",json={
         "email":"test@gmail.com","password":"123456"
         }

                 )
     token=login_response.json()["access_token"]
     headers={"Authorization":f"Bearer {token}"}
     response=client.post("/api/tasks",json={
        "title":"food","description":" Pasta","completed":False},headers=headers
                          )
     assert response.status_code==200


def test_delete_task():

    login_response=client.post("/api/login",json={
        "email":"test@gmail.com","password":"123456"

        }
                               )

    token=login_response.json()["access_token"]
    headers={"Authorization":f"Bearer {token}"}

    create_response=client.post("api/tasks",json={"title":"food","description":"Pasta","completed":False},headers=headers)

    print(create_response.json())

    task_id=create_response.json()["id"]

    response=client.delete(f"/api/tasks/{task_id}",headers=headers)

    assert response.status_code==200


def test_unauthorized_access():

    response = client.get("/api/tasks")

    assert response.status_code == 401


                
