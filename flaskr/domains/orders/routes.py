from flask import request

from flaskr.core.base.routes import BaseRoutes
from flaskr.domains.orders.services import OrderService

from . import bp


class OrderListAPI(BaseRoutes):
    service = OrderService()

    def get(self):
        order_data = self.service.list_items()
        return self.format_response(data=order_data)

    def post(self):
        data = request.get_json()
        self.service.create_new_order(
            user_id=data.get("user_id"),
            table_id=data.get("table_id"),
            items=data.get("items"),
        )
        response = data
        return response, 201


class OrderItemsAPI(BaseRoutes):
    service = OrderService()

    def get(self, order_id: int):
        response = self.service.get_by_Order_id_orderdetails(order_id=order_id)
        return self.format_response(data=response)


class OrderUpdateAPI(BaseRoutes):
    service = OrderService()

    def patch(self, order_id: int, product_id: int):
        data = request.get_json()
        quantity = data.get("quantity")
        unit_price = data.get("unit_price")
        response = self.service.update_order_products(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )

        return self.format_response(data=response)


class OrderDetailAPI(BaseRoutes):
    service = OrderService()

    def get(self, order_id: int):
        user = self.service.get_by_id(item_id=order_id)
        return self.format_response(data=user)

    def delete(self, order_id: int):
        response = self.service.delete_order_products(item_id=order_id)
        return self.format_response(data={"deletion": response})


bp.add_url_rule(
    "/", view_func=OrderListAPI.as_view("order_list_api"), methods=["GET", "POST"]
)

bp.add_url_rule(
    "/<int:order_id>",
    view_func=OrderDetailAPI.as_view("order_detail_api"),
    methods=["GET", "DELETE"],
)
bp.add_url_rule(
    "/<int:order_id>/items/<int:product_id>",
    view_func=OrderUpdateAPI.as_view("order_update_api"),
    methods=["PATCH"],
)


bp.add_url_rule(
    "/<int:order_id>/items",
    view_func=OrderItemsAPI.as_view("order_items_api"),
    methods=["GET"],
)
