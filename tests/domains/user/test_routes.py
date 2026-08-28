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
        token = res.json["data"]["access_token"]
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

    def test_create_user_returns_400(self):
        res = self.client.post(
            "/users/",
            json={
                "username": "d",
                "password": "s",
                "display_name": "s",
                "email": "baba@",
            },
            headers=self.get_auth_headers(),
        )

        assert res.status_code == 400
        assert res.json["error"] == "Validation Error"
        assert res.json["message"] == {
            "username": ["Length must be between 3 and 32."],
            "password": ["Length must be between 6 and 128."],
            "display_name": ["Length must be between 3 and 16."],
            "email": ["Not a valid email address."],
            "role_id": ["Missing data for required field."],
        }
        assert res.json["code"] == 400

    def test_get_all_users(self):
        res = self.client.get("/users/", headers=self.get_auth_headers())

        assert res.status_code == 200
        assert res.json["count"] == 1

    def test_get_specified_user(self):
        create_res = self.client.post(
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
        created_user_id = create_res.json["data"]["id"]

        res = self.client.get(
            f"/users/{created_user_id}", headers=self.get_auth_headers()
        )

        assert res.status_code == 200
        assert res.json["data"]["id"] == created_user_id

    def test_patch_user(self):
        create_res = self.client.post(
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
        created_user_id = create_res.json["data"]["id"]

        res = self.client.patch(
            f"/users/{created_user_id}",
            json={
                "username": "refactored",
                "password": "sifre123",
                "display_name": "Samsun",
                "email": "samsun@gmail.com",
                "role_id": self.role_id,
            },
            headers=self.get_auth_headers(),
        )

        assert res.status_code == 200
        assert res.json["data"]["id"] == created_user_id
        assert res.json["data"]["username"] == "refactored"

    def test_delete_user(self):
        user_res = self.client.get("/users/", headers=self.get_auth_headers()).json[
            "data"
        ][0]["id"]

        res = self.client.delete(f"/users/{user_res}", headers=self.get_auth_headers())

        assert res.status_code == 204
