from flask import request

from flaskr.core.base.routes import BaseRoutes
from flaskr.domains.product.services import ProductService
from flaskr.domains.product.validators import (
    ProductCreateValidator,
    ProductUpdateValidator,
)

from . import bp


class ProductListAPI(BaseRoutes):
    service = ProductService()

    def get(self):
        users_data = self.service.list_items()
        return self.format_response(data=users_data)

    def post(self):
        data = ProductCreateValidator().validate_data(request.get_json())
        new_product = self.service.create_new_product(data=data)

        response = self.format_response(data=new_product)
        return response, 201


class ProductDetailAPI(BaseRoutes):
    service = ProductService()

    def get(self, product_id: int):
        product = self.service.get_by_id(item_id=product_id)
        return self.format_response(data=product)

    def patch(self, product_id: int):
        data = ProductUpdateValidator().validate_data(request.get_json())

        response = self.service.update_item(item_id=product_id, data=data)
        return self.format_response(data=response)

    def delete(self, product_id: int):
        response = self.service.delete_item(item_id=product_id)
        return self.format_response({"deletion": response})


bp.add_url_rule(
    "/",
    view_func=ProductListAPI.as_view("product_list"),
    methods=["GET", "POST"],
)

bp.add_url_rule(
    "/<int:product_id>",
    view_func=ProductDetailAPI.as_view("product_detail"),
    methods=["GET", "PATCH", "DELETE"],
)
