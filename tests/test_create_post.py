from app.models import Post


def test_success_flow(client, db_session):
    payload = {"title": "test", "description": "test2"}
    response = client.post("posts/create", json=payload)

    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert db_session.query(Post).filter(Post.id == response.json()["id"]).first()

    for key in ["id", "created_at", "updated_at"]:
        assert key in response.json()


def test_invalid_payload(client, db_session):
    initial_count = db_session.query(Post).count()
    payload = {"title": "test"}
    response = client.post("posts/create", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {"title": "test"},
                "loc": ["body", "description"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
    assert db_session.query(Post).count() == initial_count


def test_empty_payload(client, db_session):
    initial_count = db_session.query(Post).count()
    payload = {}
    response = client.post("posts/create", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "title"],
                "msg": "Field required",
                "type": "missing",
            },
            {
                "input": {},
                "loc": ["body", "description"],
                "msg": "Field required",
                "type": "missing",
            },
        ]
    }
    assert db_session.query(Post).count() == initial_count


def test_title_length_with_more_than_100_chars(client, faker, db_session):
    initial_count = db_session.query(Post).count()
    payload = {"title": "a" * 101, "description": faker.text()}
    response = client.post("posts/create", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_long",
                "loc": ["body", "title"],
                "msg": "String should have at most 100 characters",
                "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "ctx": {"max_length": 100},
            }
        ]
    }
    assert db_session.query(Post).count() == initial_count


def test_description_length_more_than_500_chars(client, faker, db_session):
    initial_count = db_session.query(Post).count()
    payload = {"title": faker.sentence(), "description": "a" * 501}
    response = client.post("posts/create", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "string_too_long",
                "loc": ["body", "description"],
                "msg": "String should have at most 500 characters",
                "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "ctx": {"max_length": 500},
            }
        ]
    }
    assert db_session.query(Post).count() == initial_count
