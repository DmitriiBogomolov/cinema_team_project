from typing import Tuple
from http import HTTPStatus

from flask import Blueprint
from flask.wrappers import Response


auth = Blueprint('auth', __name__)


@auth.route('', methods=('GET',))
def test() -> Tuple[Response, HTTPStatus]:
    return 'hello world', HTTPStatus.CREATED
