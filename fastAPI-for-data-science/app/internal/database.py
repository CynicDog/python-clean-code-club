from ..models.post import Post

# mock db
mock_db = {
    i: Post(
        id=i,
        title=f"Post Number {i}",
        content=f"This is the programmatically generated content for post {i}.",
        views=i * 2
    )
    for i in range(1, 51)
}