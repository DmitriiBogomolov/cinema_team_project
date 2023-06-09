import string
import secrets
from PIL import ImageFont, ImageDraw, Image
from itertools import cycle


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
