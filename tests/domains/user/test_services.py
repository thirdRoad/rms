import pytest
from werkzeug.exceptions import NotFound

from flaskr.domains.role.models import Role
from flaskr.domains.user.services import UserService
from tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    domain_class = UserService
    domain: UserService

    def test_get_by_id_not_found(self):
        with self.app.test_request_context():
            with pytest.raises(NotFound) as exc_info:
                self.domain.get_by_id(55)

            assert exc_info.value.code == 404
            assert "There is no user" in exc_info.value.description

    def test_create_new_user(self):
        role = Role(name="admin")
        self.db.session.add(role)
        self.db.session.commit()

        with self.app.test_request_context():
            test_data = {
                "username": "denizbaba",
                "password": "asd123",
                "display_name": "BABA",
                "email": "baba@gmail.com",
                "role_id": 1,
            }
            test_response = self.domain.create_new_user(data=test_data)
            assert test_response["id"] == 1
            assert test_response["username"] == "denizbaba"
