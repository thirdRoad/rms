from flaskr.core.base.routes import BaseRoutes
from flaskr.core.decorators import role_required
from flaskr.domains.role.services import RoleService

from . import bp


class RoleListAPI(BaseRoutes):
    service = RoleService()

    @role_required("admin")
    def get(self):  # Return all roles
        roles_data = self.service.list_items()
        return self.format_plural_response(data=roles_data)


bp.add_url_rule("/", view_func=RoleListAPI.as_view("role_list_api"), methods=["GET"])
