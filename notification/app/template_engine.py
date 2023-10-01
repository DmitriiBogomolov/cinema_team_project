import jinja2

from app.errors import WrongTemplateException


async def render_email(template_data: list[dict], template_str: str) -> list[str]:
    try:
        template = jinja2.Template(template_str)
        return [template.render(**data) for data in template_data]
    except jinja2.exceptions.UndefinedError:
        raise WrongTemplateException
