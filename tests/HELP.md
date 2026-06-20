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

## Running Tests

### With Docker

- First, get inside the container.
```bash
docker exec -it rms.flask.dev bash
```

- After than, run the unit-test
```bash
pytest tests/domains/<domain>/test_routes
```
