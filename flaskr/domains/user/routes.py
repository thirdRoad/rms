from flask import request

from flaskr.core.base.routes import BaseRoutes
from flaskr.domains.user.services import UserService
from flaskr.domains.user.validators import UserCreateValidator, UserUpdateValidator

from . import bp


class UserListAPI(BaseRoutes):
    service = UserService()

    def get(self):  # Return all users
        users_data = self.service.list_items()
        return self.format_response(data=users_data)

    def post(self):
        data = UserCreateValidator().validate_data(request.get_json())
        new_user = self.service.create_new_user(data=data)

        response = self.format_response(data=new_user)
        return response, 201


class UserDetailAPI(BaseRoutes):
    service = UserService()

    def get(self, user_id: int):
        user = self.service.get_by_id(item_id=user_id)
        return self.format_response(data=user)

    def patch(self, user_id: int):
        data = UserUpdateValidator().validate_data(request.get_json())

        response = self.service.update_item(item_id=user_id, data=data)
        return self.format_response(data=response)

    def delete(self, user_id: int):
        response = self.service.delete_item(item_id=user_id)
        return self.format_response({"deletion": response})


bp.add_url_rule(
    "/", view_func=UserListAPI.as_view("user_list_api"), methods=["GET", "POST"]
)

bp.add_url_rule(
    "/<int:user_id>",
    view_func=UserDetailAPI.as_view("user_detail_api"),
    methods=["GET", "PATCH", "DELETE"],
)
