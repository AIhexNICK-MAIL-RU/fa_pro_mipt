"""Модуль тестирования"""
from random import randint
from fastapi.testclient import TestClient
import faker
from app.main import app


client = TestClient(app)
fake = faker.Faker()

#client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_login = fake.first_name()
client.fake_title = " ".join(fake.words(2))
client.fake_author = f"{fake.first_name()} {fake.first_name()}"
client.fake_genre = fake.word(ext_word_list=("pop", "rock", "jazz", "classic"))
client.fake_estimate = randint(1,5)
client.new_user_id = 0
client.auth_token = ""
client.new_track_id = 0


def test_create_user():
    """Тест создания пользователя"""
    response = client.post("/users/create_user",
                           json={"login": client.fake_login,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 201
    assert response.json()['message'] == "Пользователь зарегистрирован"
    # client.new_user_id = response.json()['id']


def test_token():
    """Тест получения токена"""
    response = client.post("/users/token",
                           data={"username": client.fake_login,
                                 "password": client.fake_user_password}
    )
    assert response.status_code == 200
    client.auth_token = response.json()['access_token']

def test_create_track():
    """Тест создания трека"""
    response = client.post("/tracks/create_track",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"title": client.fake_title,
                                 "author": client.fake_author,
                                 "genre": client.fake_genre}
    )
    assert response.status_code == 201
    client.new_track_id = response.json()['id']

def test_set_rating():
    """Тест создания оценки"""
    response = client.patch("/ratings/set_rating",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"track_id": client.new_track_id,
                                "estimate": client.fake_estimate})
    assert response.status_code == 201
    assert response.json()['track_id'] == client.new_track_id

def test_change_rating():
    """Тест изменения оценки"""
    response = client.patch("/ratings/change_rating",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"track_id": client.new_track_id,
                                "estimate": client.fake_estimate})
    assert response.status_code == 201

def test_set_rating_fail():
    """Тест создания оценки"""
    response = client.patch("/ratings/set_rating",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"track_id": 0, # предполагается, что такого трека не будет
                                "estimate": client.fake_estimate})
    assert response.status_code == 404


def test_create_track_fail():
    """Тест неудачного создания трека"""
    response = client.post("/tracks/create_track",
                           headers={"Authorization": f"Bearer {client.auth_token}"},
                           json={"title": client.fake_title,
                                 "author": client.fake_author,
                                 "genre": client.fake_genre}
    )
    assert response.status_code == 400


def test_get_full_list():
    """Тест получения списка треков"""
    response = client.get("/tracks/get_full_list")
    assert response.status_code == 200


def test_delete_track():
    """Тест удаления трека"""
    response = client.delete("/tracks/delete_track",
                             headers={"Authorization": f"Bearer {client.auth_token}"},
                             params={"track_id": client.new_track_id})
    assert response.status_code == 204


def test_delete_track_fail():
    """Тест неудачного удаления трека"""
    response = client.delete("/tracks/delete_track",
                             headers={"Authorization": f"Bearer {client.auth_token}"},
                             params={"track_id": client.new_track_id})
    assert response.status_code == 400

def test_get_main():
    """Тест начальной страницы"""
    response = client.get("/")
    assert response.status_code == 200


def test_get_my_recommend():
    """Тест получения рекомендаций"""
    response = client.get("/ratings/get_my_recommendations",
                          params={"user_id": client.new_user_id})
    assert response.status_code == 200
