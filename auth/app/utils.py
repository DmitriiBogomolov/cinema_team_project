import string
import secrets

from flask import request, session
from PIL import ImageFont, ImageDraw, Image
from itertools import cycle

from app.error_handlers.exceptions import (
    NoCaptchaError,
    WrongCaptchaError
)
from config import config


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(10))
    return password


def generate_captcha(code_captcha: str, width: int, height: int):
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # подгружаем шрифты
    font = ImageFont.truetype('font/1979_dot_matrix.ttf', size=40)
    gen_point = cycle([10, 55])
    x, y = 0, 0
    # генерируем каждый символ каптчи по выбранным координатам
    for let in code_captcha:
        if x == 0:
            x = 5
        else:
            x = x + width / 5
        y = next(gen_point)
        # наносим символ
        draw.text((x, y), let, font=font, fill=False)

    # Генерируем шум на картинке
    diff = 0
    for _ in range(max(width, height)):
        diff += 2
        draw.line((0, diff, 200, diff), fill=False, width=1)
    return img


def handle_captcha(func):
    """Сompares the captcha from the session and the request body."""
    def wrapper(*args, **kwargs):
        if config.debug or request.method == 'GET':
            return func(*args, **kwargs)

        sess_captcha = session.get('captcha')
        input_captcha = request.get_json().get('captcha')
        if not sess_captcha or not input_captcha:
            raise NoCaptchaError
        elif sess_captcha.lower() != input_captcha.lower():
            raise WrongCaptchaError

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
