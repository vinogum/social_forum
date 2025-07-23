import pytest


@pytest.mark.django_db
def test_create_post(api_client, valid_file):
    data = {"title": "title", "text": "text", "images": [valid_file]}
    response = api_client.post("/posts/", data, format="multipart")
    assert response.status_code == 201


@pytest.mark.django_db
def test_list_post(api_client):
    response = api_client.get("/posts/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_retrieve_post(api_client, post):
    response = api_client.get(f"/posts/{post.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_post(api_client, post):
    data = {"title": "newtitle", "text": "newtext"}
    response = api_client.patch(f"/posts/{post.id}/", data)
    assert response.status_code == 200

    post.refresh_from_db()
    assert post.title == "newtitle"
