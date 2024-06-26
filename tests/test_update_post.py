from app.models import Post


def create_post(db):
    post = Post(**({"title": "Hello", "description": "World"}))
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def test_success_flow(client, db_session, faker):
    post = create_post(db_session)
    payload = {"title": faker.sentence(), "description": faker.sentence()}
    response = client.put(f"posts/{post.id}", json=payload)

    # Check if the response status code is 201
    assert response.status_code == 200

    # Check if the response contains the title and description
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]

    # Check if the response contains the id, created_at, and updated_at fields
    for key in ["id", "created_at", "updated_at"]:
        assert key in response.json()

    # Check if the post was updated in the database
    new_post = db_session.query(Post).filter(Post.id == post.id).first()
    assert new_post.title == payload["title"]
    assert new_post.description == payload["description"]


def test_empty_payload(client, db_session):
    post = create_post(db_session)
    response = client.put(f"posts/{post.id}", json={})

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

    # Check if the post was not mutated
    new_post = db_session.query(Post).filter(Post.id == post.id).first()
    assert new_post.title == post.title
    assert new_post.description == post.description


def test_fails_on_title_length_more_than_100_chars(client, faker, db_session):
    post = create_post(db_session)
    payload = {"title": "a" * 101, "description": faker.text()}
    response = client.put(f"posts/{post.id}", json=payload)

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

    # Check if the post was not mutated
    new_post = db_session.query(Post).filter(Post.id == post.id).first()
    assert new_post.title == post.title
    assert new_post.title != payload["title"]
    assert new_post.description == post.description
    assert new_post.description != payload["description"]


def test_fails_on_description_length_more_than_500_chars(client, faker, db_session):
    post = create_post(db_session)
    payload = {"title": faker.sentence(), "description": "a" * 501}
    response = client.put(f"posts/{post.id}", json=payload)

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

    # Check if the post was not mutated
    new_post = db_session.query(Post).filter(Post.id == post.id).first()
    assert new_post.title == post.title
    assert new_post.title != payload["title"]
    assert new_post.description == post.description
    assert new_post.description != payload["description"]
