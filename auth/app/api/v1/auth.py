from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify
from flask.wrappers import Response

auth = Blueprint('auth', __name__)


@auth.route('', methods=('GET',))
def test() -> Tuple[Response, HTTPStatus]:
    """ТЕСТОВЫЕ РУЧКИ"""
    return jsonify('hello world'), HTTPStatus.CREATED
