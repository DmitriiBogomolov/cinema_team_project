import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from email.message import EmailMessage
from config.jinja2_template import get_jinja_template
from config.config import worker_email_config


class MessageEmail:
    def __init__(self, message: EmailMessage):
        self.message = message
        self.message['From'] = worker_email_config.get_email_from()

    def get_message_email(self, data: dict, path_template: str, teplate_message: dict):
        self.message['To'] = data['email']
        self.message['Subject'] = teplate_message['subject']

        teplate_message['text'] = teplate_message['text'].substitute(data)
        template = get_jinja_template(path_template)
        output = template.render(**teplate_message)
        self.message.add_alternative(output, subtype='html')
        return self.message
