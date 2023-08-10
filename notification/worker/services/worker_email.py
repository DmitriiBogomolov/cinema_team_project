import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import copy
import datetime
import smtplib
import json
import motor.motor_asyncio
from email.message import EmailMessage
from config.config import mongo_config, worker_email_config
from data_message import TEMPLATE_TEXT
from prepear.prepear_email_worker import MessageEmail


def callback_email(ch, method, properties, body):
    message = EmailMessage()
    message_email = MessageEmail(message)
    data = json.loads(body)

    event = data['event_name']
    to_email = data['email']
    path_template = f'templates/{event}.html'
    template_text = copy.deepcopy(TEMPLATE_TEXT)
    teplate_message = template_text[event]
    message = message_email.get_message_email(data, path_template, teplate_message)

    with smtplib.SMTP_SSL(worker_email_config.smtp_host, worker_email_config.smtp_port) as server:
        server.login(worker_email_config.login, worker_email_config.password)

        try:
            server.sendmail(worker_email_config.get_email_from(), [to_email], message.as_string())
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            print(f'Не удалось отправить письмо. {reason}')
        else:
            print('Письмо отправлено!')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            client = motor.motor_asyncio.AsyncIOMotorClient(mongo_config.uri)
            client.notification.events.update_one({'_id': data['id']},
                                                  {'$set': {'send_message_date': datetime.datetime.now()}})
