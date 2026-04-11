from flaskr.core.extensions import db
from flaskr.domains.role.models import Role
from tests.base import BaseTestCase


class TestUserListAPI(BaseTestCase):

    def setup_case(self):
        role = Role(name="admin")
        db.session.add(role)
        db.session.commit()
        self.role_id = role.id

    def test_create_user_returns_201(self):
        res = self.client.post(
            "/users/",
            json={
                "username": "denizbaba",
                "password": "asd123",
                "display_name": "BABA",
                "email": "baba@gmail.com",
                "role_id": self.role_id,
            },
        )

        assert res.status_code == 201
        assert res.json()["response"]["username"] == "denizbaba"
        assert res.json()["response"]["email"] == "baba@gmail.com"
        assert "password" not in res.json()["response"]
