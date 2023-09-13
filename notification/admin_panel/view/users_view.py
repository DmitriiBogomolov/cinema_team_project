from flask_admin.contrib.sqlamodel import ModelView


class EventView(ModelView):
    column_list = ('event_name', 'template', 'condition')
