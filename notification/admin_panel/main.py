from flask import Flask
from flask_admin import Admin

from models import db, Event
from view.users_view import EventView


def create_app():

    app = Flask(__name__)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app:123qwe@localhost:5432/notification_database'
    app.config['SECRET_KEY'] = 'DdsfIndmfm54559'

    admin = Admin(app, name='admin panel', template_mode='bootstrap3')
    admin.add_view(EventView(Event, db.session))

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000)
