from flask import request
from app.schemas import SignInEntrieSchema
from app.models import User


def save_signin_entrie(user: User, request: request):
    """Save a record to user log-in history"""
    schema = SignInEntrieSchema()
    entrie = schema.load({
        'user_id': user.id,
        'user_agent': request.user_agent.string,
        'remote_addr': request.environ['REMOTE_ADDR']
    })
    entrie.save()
