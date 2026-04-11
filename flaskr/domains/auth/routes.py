from flask import Response, jsonify, request

from flaskr.core.base.routes import BaseRoutes
from flaskr.domains.auth.services import AuthService
from flaskr.domains.auth.validators import AuthLoginValidator

from . import bp


class AuthLoginAPI(BaseRoutes):
    service: AuthService = AuthService()

    @staticmethod
    def format_response(data: str, pagination: bool = False) -> Response:
        response = {
            "access_token": data,
        }
        return jsonify(response)

    def post(self):
        data = AuthLoginValidator().validate_data(data=request.get_json())
        token = self.service.verify_user(
            username=data["username"], password=data["password"]
        )
        return self.format_response(data=token)


bp.add_url_rule(
    "/login", view_func=AuthLoginAPI.as_view("auth_login_api"), methods=["POST"]
)
