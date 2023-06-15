from random import choice
from io import BytesIO

from flask import (
    Blueprint,
    session,
)

from app.helpers.captcha import generate_captcha


captcha = Blueprint('captcha', __name__)


@captcha.route('', methods=['GET'])
def get_captcha(width: int = 200, height: int = 100) -> bytes:
    """Generates captcha image"""
    code = ''.join([choice('QERTYUPLKJHGFDSAZXCVBN23456789') for i in range(5)])
    # сгенерированный код пишем в сессию
    session['captcha'] = code
    img = generate_captcha(code, width, height)
    buff = BytesIO()
    img.save(buff, 'png')
    return buff.getvalue()
