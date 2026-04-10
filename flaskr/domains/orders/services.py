from typing import Any, List

from flask import abort

from flaskr.core.base.services import BaseService
from flaskr.core.extensions import db
from flaskr.domains.orderDetails.models import OrderDetail
from flaskr.domains.orderDetails.repository import OrderDetailsRepository
from flaskr.domains.orders.models import Order
from flaskr.domains.orders.repository import OrderRepository
from flaskr.domains.product.repositories import ProductRepository
from flaskr.domains.tables.repositories import TableRepository


class OrderService(BaseService):
    repository: OrderRepository
    repository = OrderRepository()
    order_detail_repo = OrderDetailsRepository()
    product_repo = ProductRepository()
    table_repo = TableRepository()

    def get_by_id(self, item_id: int) -> Any | None:
        order = self.repository.get_by_id(item_id=item_id)

        if order is None:
            abort(404, description="Order not found")

        response = order.serialize
        response["user"] = {
            "id": order.user.id,
            "username": order.user.username,
            "email": order.user.email,
            "created_at": order.created_at,
            "display_name": order.user.display_name,
        }
        return response

    def get_by_Order_id_orderdetails(self, order_id: int) -> List[OrderDetail]:
        orders = self.order_detail_repo.get_by_order_id(order_id)

        if orders is None:
            abort(404, description="Order not found")

        response = []

        for order in orders:
            response.append(order.serialize)

        return response

    def create_new_order(self, user_id: int, table_id: int, items: list):
        order = Order(
            user_id=user_id,
            table_id=table_id,
        )
        db.session.add(order)
        db.session.flush()

        details_to_add = []
        for item in items:
            product = self.product_repo.get_by_id(item["product_id"])
            if product:
                details_to_add.append(
                    {
                        "product_id": product.id,
                        "quantity": item["quantity"],
                        "unit_price": product.price,
                    }
                )

        self.order_detail_repo.add_bulk(order.id, details_to_add)

        db.session.commit()

        return order.serialize

    def update_order_products(
        self, order_id: int, product_id: int, quantity: int, unit_price: float
    ):
        order = self.repository.get_by_id(order_id)

        if order is None:
            abort(404, description="Order not found")

        product = self.product_repo.get_by_id(product_id)

        if product is None:
            abort(404, description="Product not found")

        self.order_detail_repo.upsert_item(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )

        db.session.commit()
        return product.serialize

    def delete_order_products(self, item_id: int) -> bool:
        try:
            result = self.order_detail_repo.delete_all_by_order_id(item_id)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
