import json
from http import HTTPStatus

from flask import Blueprint, request
from flask.wrappers import Response
from app.models import User
from app.core.pre_configured.token_auth import token_auth
from app.model_api import ContactsUser
from app.api.v1.catchers import default_exception_catcher


enrichment = Blueprint('enrichment', __name__)


@enrichment.route('/info_users', methods=('POST',))
@token_auth.login_required
@default_exception_catcher
def get_data_client() -> tuple[Response, HTTPStatus]:
    """Getting email"""
    ids = request.get_json().get('ids')
    if isinstance(ids, list):
        users = User.get_by_list_users(ids)
        response = [ContactsUser(id=str(user.id), email=user.email).dict() for user in users]
        return json.dumps(response), HTTPStatus.OK

    user = User.get_by_id(ids)
    response = ContactsUser(id=user.id, email=user.email)
    return response.json(), HTTPStatus.OK
