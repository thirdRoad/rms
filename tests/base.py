from typing import Generic, Type, TypeVar

from flask import Flask
from flask.ctx import AppContext
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.core.extensions import db

T = TypeVar("T")


class BaseTestCase(Generic[T]):
    domain_class: Type[T]
    domain: T

    app: Flask
    client: FlaskClient
    ctx: AppContext
    db: SQLAlchemy

    def generate_generic_class(self):
        self.domain = self.domain_class()

    def setup_case(self):
        pass

    def setup_method(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.db = db
        self.ctx.push()
        db.create_all()
        self.generate_generic_class()
        self.setup_case()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
