from app.models import Post


def test_success_flow(client, db_session):
    payload = {"title": "Hello", "description": "World"}
    response = client.post("posts", json=payload)

    # Check if the response status code is 201
    assert response.status_code == 201

    # Check if the response contains the title and description
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]

    # Check if the response contains the id, created_at, and updated_at fields
    for key in ["id", "created_at", "updated_at"]:
        assert key in response.json()

    # Check if the post was created in the database
    assert db_session.query(Post).filter(Post.id == response.json()["id"]).first()


def test_empty_payload(client, db_session):
    initial_count = db_session.query(Post).count()
    response = client.post("posts", json={})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "title"],
                "msg": "Field required",
                "type": "missing",
                "input": {},
            },
            {
                "loc": ["body", "description"],
                "msg": "Field required",
                "type": "missing",
                "input": {},
            },
        ]
    }

    assert db_session.query(Post).count() == initial_count


def test_fails_on_title_length_more_than_100_chars(client, faker, db_session):
    payload = {"title": "a" * 101, "description": faker.text()}
    response = client.post("posts", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_long",
                "loc": ["body", "title"],
                "msg": "String should have at most 100 characters",
                "input": payload["title"],
                "ctx": {"max_length": 100},
            }
        ]
    }

    # Check if the post was created in the database
    assert db_session.query(Post).filter(Post.title == payload["title"]).first() is None


def test_fails_on_description_length_more_than_500_chars(client, faker, db_session):
    payload = {"title": faker.sentence(), "description": "a" * 501}
    response = client.post("posts", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_long",
                "loc": ["body", "description"],
                "msg": "String should have at most 500 characters",
                "input": payload["description"],
                "ctx": {"max_length": 500},
            }
        ]
    }

    # Check if the post was created in the database
    assert (
        db_session.query(Post)
        .filter(Post.description == payload["description"])
        .first()
        is None
    )
