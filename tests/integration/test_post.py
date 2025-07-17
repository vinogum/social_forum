import pytest


@pytest.mark.django_db
def test_create_post(api_client, valid_file):
    data = {"title": "title", "text": "text", "images": [valid_file]}
    response = api_client.post("/posts/", data, format="multipart")
    assert response.status_code == 201
