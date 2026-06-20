from werkzeug.security import generate_password_hash

from flaskr.core.extensions import db
from flaskr.domains.role.models import Role
from flaskr.domains.user.models import User
from flaskr.domains.user.services import UserService
from tests.base import BaseTestCase


class TestUserListAPI(BaseTestCase):
    domain_class = UserService
    domain: UserService

    def setup_case(self):
        role = Role(name="admin")
        db.session.add(role)
        db.session.commit()
        self.role_id = role.id

        admin_user = User(
            username="testadmin",
            password=generate_password_hash("adminpass"),
            display_name="Admin",
            email="admin@test.com",
            role_id=self.role_id,
        )
        db.session.add(admin_user)
        db.session.commit()

    def get_auth_headers(self) -> dict:
        res = self.client.post(
            "/auth/login",
            json={"username": "testadmin", "password": "adminpass"},
        )
        token = res.json["access_token"]
        return {"Authorization": f"Bearer {token}"}

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
            headers=self.get_auth_headers(),
        )

        assert res.status_code == 201
        assert res.json["data"]["username"] == "denizbaba"
        assert res.json["data"]["email"] == "baba@gmail.com"
        assert "password" not in res.json["data"]
