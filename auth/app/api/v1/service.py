import json
from http import HTTPStatus

from flask import Blueprint, request
from flask.wrappers import Response
from app.models import User
from app.core.pre_configured.token_auth import token_auth
from app.model_api import ServiceUser
from app.api.v1.catchers import default_exception_catcher


service = Blueprint('service', __name__)


@service.route('/email', methods=('POST',))
@token_auth.login_required
@default_exception_catcher
def get_data_client() -> tuple[Response, HTTPStatus]:
    """Getting email"""
    ids = request.get_json().get('ids')
    if isinstance(ids, list):
        users = User.get_by_list_users(ids)
        answer_users = [ServiceUser(id=str(user.id), email=user.email).dict() for user in users]
        return json.dumps(answer_users), HTTPStatus.OK

    user = User.get_by_id(ids)
    answer_user = ServiceUser(id=user.id, email=user.email)
    return answer_user.json(), HTTPStatus.OK
