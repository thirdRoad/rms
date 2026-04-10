from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


class ErrorHandler:
    @staticmethod
    def init_app(app):
        @app.errorhandler(Exception)
        def handle_exception(e):
            if isinstance(e, ValidationError):
                return (
                    jsonify(
                        {
                            "error": "Validation Error",
                            "message": e.messages,
                            "code": 400,
                        }
                    ),
                    400,
                )

            if isinstance(e, HTTPException):
                response = {"error": e.name, "message": e.description, "code": e.code}
                return jsonify(response), e.code

            response = {
                "error": "Internal Server Error",
                "message": f"Flask error: {e}",
                "code": 500,
            }
            return jsonify(response), 500
