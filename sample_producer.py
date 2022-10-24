import gzip
import json
from pika import BasicProperties
import pika
import logging
import sys
import uuid


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s (%(filename)s:%(funcName)s:%(lineno)d) [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("Reports")


def receiveMessage(channel, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    logger.info(message)
    if channel.is_open:
        channel.basic_ack(method.delivery_tag)


amqp_url = 'amqp://guest:guest@127.0.0.1:5672'
urlConnectionParameters = pika.URLParameters(amqp_url)
parameters = urlConnectionParameters

connection = pika.BlockingConnection(parameters)
logger.info('[x] built a connection')
channel = connection.channel()
channel.queue_declare(queue='foo.adda', durable=True)
channel.queue_declare(queue='foo.adda.out', durable=True)
channel.exchange_declare('celery_reports', exchange_type='direct',passive=False, durable=True, 
                         auto_delete=False, internal=False, arguments=None# , callback=None
                         )
channel.queue_bind(queue='foo.adda.out', exchange='celery_reports',
                   routing_key='foo.adda.out'  # , arguments=None, callback=None
                   )

reply_to = 'foo.adda.out'
correlation_id = "55229900"

header_id = str(uuid.uuid4())
# for i in range(100):
correlation_id = str(111333222)
input_task = {'to_sum': [1, 8, 2, -3, 5]}

channel.basic_publish(exchange='celery_reports',
                      routing_key='foo.adda',
                      body=json.dumps(input_task, default=str).encode('utf-8'),
                      properties=BasicProperties(
                          correlation_id=correlation_id,
                          content_type='application/data',
                          content_encoding='utf-8',
                          reply_to=reply_to,
                          headers={'task': 'foo.adda',
                                   'id': header_id})
                    )
logger.info(f"sent id: {header_id}")
channel.basic_consume(queue='foo.adda.out', no_ack=False, consumer_callback=receiveMessage)
logger.info('[x] Waiting for messages')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
finally:
    connection.close()
