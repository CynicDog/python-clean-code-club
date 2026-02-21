import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_create_post(client: AsyncClient):
    """Test creating a new post successfully."""

    payload = {"title": "Test Post", "content": "This is a test content"}
    response = await client.post("/posts/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


@pytest.mark.asyncio
async def test_read_post_not_found(client: AsyncClient):
    """Test retrieving a post that doesn't exist."""

    response = await client.get("/posts/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post not found"


@pytest.mark.asyncio
async def test_create_and_get_post(client: AsyncClient):
    """Test the flow of creating a post and then fetching it by ID."""

    create_resp = await client.post(
        "/posts/", json={"title": "Find Me", "content": "Content"}
    )
    post_id = create_resp.json()["id"]

    get_resp = await client.get(f"/posts/{post_id}")
    assert get_resp.status_code == status.HTTP_200_OK
    assert get_resp.json()["title"] == "Find Me"


@pytest.mark.asyncio
async def test_list_all_posts(client: AsyncClient):
    """Test the /all endpoint."""

    await client.post("/posts/", json={"title": "Post 1", "content": "C1"})

    response = await client.get("/posts/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient):
    """Test deleting a post."""

    create_resp = await client.post(
        "/posts/", json={"title": "To Delete", "content": "..."}
    )
    post_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/posts/{post_id}")
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    get_resp = await client.get(f"/posts/{post_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_comment(client: AsyncClient):
    """Test adding a comment to a specific post."""

    post_resp = await client.post(
        "/posts/", json={"title": "Post for Comment", "content": "..."}
    )
    post_id = post_resp.json()["id"]

    comment_payload = {"content": "Great post!"}
    response = await client.post(f"/posts/{post_id}/comments", json=comment_payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["content"] == "Great post!"
