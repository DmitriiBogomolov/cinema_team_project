from flask import Request

from app.models import User
from app.schemas import SignInEntrieSchema


class SignInJournal:
    def save_sign_in_entrie(self, user: User, request: Request):
        schema = SignInEntrieSchema()
        entrie = schema.load({
            'user_id': user.id,
            'user_agent': request.user_agent.string,
            'remote_addr': request.environ['REMOTE_ADDR']
        })
        user.sign_in_entries.append(entrie)
        user.save()


journal = SignInJournal()
