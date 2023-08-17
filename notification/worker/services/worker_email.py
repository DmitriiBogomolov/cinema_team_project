import os
import sys
import smtplib
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import datetime
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import motor.motor_asyncio
from config.config import mongo_config, worker_email_config
from services.abstract_worker import AbstractWorker


class EmailWorker(AbstractWorker):
    def __init__(self, message=None) -> None:
        self.message = message
        self.id = None
        self.sender = None
        self.receiver = None

    def get_message(self, body):
        data = json.loads(body)
        self.sender = worker_email_config.get_email_from()
        self.receiver = data['email']
        self.message['From'] = self.sender
        self.message['To'] = self.receiver
        self.message['Subject'] = data['topic_message']
        self.message.attach(MIMEText(data['text_message'], 'plain'))

    def send_message(self, ch, method):
        smtp_host = worker_email_config.smtp_host
        smtp_port = worker_email_config.smtp_port
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.sendmail(self.sender, self.receiver, self.message.as_string())

        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            print(f'Не удалось отправить письмо. {reason}')
        else:
            print('Письмо отправлено!')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            client = motor.motor_asyncio.AsyncIOMotorClient(mongo_config.uri)
            client.notification.events.update_one({'_id': self.id},
                                                  {'$set': {'send_message_date': datetime.datetime.now()}})

    def run(self, ch, method, properties, body):
        print('Start reading...')
        self.get_message(body)
        self.send_message(ch, method)


worker_email = EmailWorker(MIMEMultipart())
