from flask import abort
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from flaskr.domains.user.models import User
from flaskr.domains.user.repositories import UserRepository


class AuthService:
    repository: UserRepository
    repository = UserRepository()

    def verify_user(self, username: str, password: str) -> str:
        user: User = self.repository.get_by_name(column_name="username", value=username)

        if not user or not check_password_hash(user.password, password):
            abort(401, description="Invalid credentials")
        else:
            return create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.role.name},
            )
