import pika
from services.worker_email import worker_email
from config.config import rabbit_config

connection = pika.BlockingConnection(pika.URLParameters(rabbit_config.uri))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
# Основная очередь
channel.queue_declare(queue='email', arguments={'x-max-priority': 10, 'x-message-ttl': 1800000})

# Обменник и очередь для писем которые получили исключения во время обработки
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')
channel.queue_declare(queue='dlx_queue')
channel.queue_bind(exchange='dlx_exchange', queue='dlx_queue', routing_key='')

channel.basic_consume(queue='email', on_message_callback=worker_email.run, auto_ack=False)
channel.start_consuming()
