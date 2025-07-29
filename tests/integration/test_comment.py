import pytest


@pytest.mark.django_db
def test_create_comment(api_client, post):
    response = api_client.post(f"/posts/{post.id}/comments/", data={"text":"sometext"}, format="json")
    assert response.status_code == 201

    data = response.json()
    assert data.get("text") is not None
    assert data["text"] == "sometext"


@pytest.mark.django_db
def test_list_comment(api_client, post, comment):
    response = api_client.get(f"/posts/{post.id}/comments/")
    assert response.status_code == 200

    comments_data = response.json()
    comment_data = comments_data[0]
    
    assert comment_data["user"] == comment.user.id
    assert comment_data["post"] == comment.post.id
    assert comment_data["text"] == comment.text


@pytest.mark.django_db
def test_update_comment(api_client, post, comment):
    response = api_client.patch(f"/posts/{post.id}/comments/{comment.id}/", format="json")
    assert response.status_code == 200
    
    data = response.json()
    comment.refresh_from_db()
    assert data["text"] == comment.text
