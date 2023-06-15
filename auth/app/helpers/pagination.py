from werkzeug.local import LocalProxy
from marshmallow import ValidationError
from flask_sqlalchemy.pagination import QueryPagination


def get_pagination_params(request: LocalProxy) -> tuple[int, int]:
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    if per_page > 1000:
        raise ValidationError('Unsupported page size (more than 1000).')
    return page, per_page


def get_pagination_meta(query: QueryPagination) -> dict:
    return {
        'page': query.page,
        'pages': query.pages,
        'total_count': query.total,
        'prev_page': query.prev_num,
        'next_page': query.next_num,
        'has_next': query.has_next,
        'has_prev': query.next_num
    }
