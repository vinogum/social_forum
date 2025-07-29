import pytest
from posts.models import Post


@pytest.mark.django_db
def test_create_post(api_client, valid_file):
    data = {"title": "title", "text": "text", "images": [valid_file]}
    response = api_client.post("/posts/", data, format="multipart")
    assert response.status_code == 201

    post_data = response.json()
    assert post_data.get("id") is not None

    post = Post.objects.get(id=post_data["id"])
    assert post_data["id"] == post.id
    assert post_data["user"] == post.user.id
    assert post_data["title"] == post.title
    assert post_data["text"] == post.text

    post_image = post.images.first() 
    assert post_image is not None
    
    expected_file_path = post_image.image_data.name
    assert post_data["images"][0]["image_data"] == expected_file_path


@pytest.mark.django_db
def test_list_post(api_client, post):
    response = api_client.get("/posts/", format="application/json")
    assert response.status_code == 200

    posts_data = response.json()
    post_data = posts_data[0]
    assert post_data["id"] == post.id
    assert post_data["user"] == post.user.id
    assert post_data["title"] == post.title
    assert post_data["text"] == post.text
    assert post_data["images"] == []


@pytest.mark.django_db
def test_retrieve_post(api_client, post):
    response = api_client.get(f"/posts/{post.id}/")
    assert response.status_code == 200

    post_data = response.json()
    assert post_data["id"] == post.id
    assert post_data["user"] == post.user.id
    assert post_data["title"] == post.title
    assert post_data["text"] == post.text
    assert post_data["images"] == []


@pytest.mark.django_db
def test_update_post(api_client, post):
    data = {"title": "newtitle", "text": "newtext"}
    response = api_client.patch(f"/posts/{post.id}/", data)
    assert response.status_code == 200

    post.refresh_from_db()
    assert post.title == "newtitle"
    assert post.text == "newtext"
