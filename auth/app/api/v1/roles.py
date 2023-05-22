from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.services.role_service import role_service
from app.schemas import RoleSchema


roles = Blueprint('roles', __name__)

role_schema = RoleSchema()


@roles.route('', methods=('GET',))
def get_roles() -> Tuple[Response, HTTPStatus]:
    """ТЕСТОВЫЕ РУЧКИ"""
    roles = role_service.get_roles()
    return jsonify(role_schema.dump(roles, many=True)), HTTPStatus.OK


@roles.route('', methods=('POST',))
def create_role() -> Tuple[Response, HTTPStatus]:
    """ТЕСТОВЫЕ РУЧКИ"""
    data = request.get_json()
    role = role_service.create_role(data)
    return jsonify(role_schema.dump(role)), HTTPStatus.CREATED
