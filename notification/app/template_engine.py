from app.base_models import BasicEvent
from app.base_models import EventNames

templates = {
    EventNames.REVIEW_COMMENT_RECEIVED: 'Hello, {{user.email}}!'
}

def render_notifications(event: BasicEvent):
    pass
