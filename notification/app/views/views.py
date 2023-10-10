from sqladmin import ModelView
from app.models.models import EmailTemlate, StoredEvent


class StoredEventView(ModelView, model=StoredEvent):
    form_include_pk = True
    form_excluded_columns = [StoredEvent.email_template]


class EmailTemlateView(ModelView, model=EmailTemlate):
    form_include_pk = True
    form_ajax_refs = {
        'event': {
            'fields': ('name', ),
        }
    }
