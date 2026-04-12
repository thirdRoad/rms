# Unit-Test Guide

## Priority
1. Route tests — covers auth, validation, status code, response format
2. Service tests — only if complex business logic exists

## Structure
```
tests/
├── base.py
└── domains/
    └── <domain>/
        ├── test_routes.py
        └── test_services.py
```

## BaseTestCase

`BaseTestCase` handles app creation, DB setup and teardown for each test.
Override `setup_case()` to seed test data — do not override `setup_method`.

```python
class TestUserListAPI(BaseTestCase):
    def setup_case(self):
        role = Role(name="admin")
        db.session.add(role)
        db.session.commit()
        self.role_id = role.id
```

## Writing Route Tests

Use `self.client` to make HTTP requests.

```python
def test_create_user_returns_201(self):
    res = self.client.post("/users/", json={...})
    assert res.status_code == 201
    assert res.json()["response"]["username"] == "denizbaba"
```

## Writing Service Tests

Use `self.app.test_request_context()` when the service calls `abort()`.

```python
def test_get_by_id_not_found(self):
    with self.app.test_request_context():
        with pytest.raises(NotFound) as exc_info:
            self.domain.get_by_id(999)
        assert exc_info.value.code == 404
```

## Running Tests

```bash
pytest tests/ -v
```
